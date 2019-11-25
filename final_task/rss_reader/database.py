import sqlite3
import time
import pkg_resources

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DATA_FILE = "data/rss.sqlite"


class DBError(Exception):
    pass


class DB:
    def __init__(self):
        path = pkg_resources.resource_filename(__name__, DATA_FILE)
        try:
            self.conn = sqlite3.connect(path)
        except sqlite3.OperationalError as e:
            raise DBError(str(e))
        self.cursor = self.conn.cursor()
        self.feed_id = None

    def _create_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS feeds")
        self.cursor.execute("DROP TABLE IF EXISTS items")
        self.cursor.execute('''
            CREATE TABLE feeds(
                id INTEGER PRIMARY KEY,
                title TEXT,
                link TEXT UNIQUE NOT NULL 
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE items(
                id INTEGER PRIMARY KEY,
                feed_id INTEGER NOT NULL, 
                published TEXT NOT NULL,
                title TEXT,
                link TEXT,
                enclosure TEXT,
                description TEXT,
                description_parsed TEXT,
                FOREIGN KEY (feed_id) REFERENCES feeds(id)
            )
        ''')
        self.cursor.execute('''
            CREATE UNIQUE INDEX un_items ON items(published, title, link)
        ''')
        self.conn.commit()

    def get_feed(self, feed_link, req_date, limit=-1):
        feed_info = self._get_feed_info_if_exists(feed_link)
        if feed_info is not None:
            req_date = time.strftime(DATE_FORMAT, req_date)

            self.cursor.execute('''
                select i.title, i.published, i.link, i.enclosure, i.description, i.description_parsed 
                    from items i join feeds f on i.feed_id = f.id 
                        where f.id=(?) and date(i.published)=date(?) limit (?)
            ''', (feed_info[0], req_date, limit)
            )

            items = []
            for i in self.cursor.fetchall():
                item = dict(title=i[0], date=time.strptime(i[1], DATETIME_FORMAT), link=i[2], enclosure=i[3],
                            description=i[4], description_parsed=i[5])
                items.append(item)
            return dict(title=feed_info[1], items=items)
        else:

            return None

    def store_feed(self, link, title, items):
        feed_id = self._get_feed_id_if_exists(link)
        if feed_id is None:
            self.cursor.execute("insert into feeds(title, link) values (?, ?)", (title, link))
            feed_id = self.cursor.lastrowid
            self.conn.commit()
        self.feed_id = feed_id
        self._store_items(items)

    def _store_items(self, items):
        for i in items:
            item_dict = dict(
                feed_id=self.feed_id,
                published=time.strftime(DATETIME_FORMAT, i["date"]),
                title=i["title"],
                link=i["link"],
                enclosure=i["enclosure"],
                description=i["description"],
                description_parsed=i["description_parsed"]
            )
            self.cursor.execute('''
            insert or ignore into items(feed_id, published, title, link, enclosure, description, description_parsed) 
                values (:feed_id, :published, :title, :link, :enclosure, :description, :description_parsed)
            ''', item_dict)
        self.conn.commit()

    def _get_feed_id_if_exists(self, feed_link):
        feed_info = self._get_feed_info_if_exists(feed_link)
        if feed_info is not None:
            return feed_info[0]
        else:
            return None

    def _get_feed_info_if_exists(self, feed_link):
        self.cursor.execute("select feeds.id, feeds.title from feeds where feeds.link=?", (feed_link,))
        feed_info = self.cursor.fetchone()
        if feed_info is not None:
            return feed_info[0], feed_info[1]
        return None


if __name__ == '__main__':
    db = DB()
    db._create_db()
