

class NewsArticle:
    """Contain data about an article"""
    def __init__(self, news_outlett_name, news_title, pub_date, news_link,
                 news_description, img_alt='', img_src=''):

        self.news_outlett_name = news_outlett_name
        self.news_title = news_title
        self.pub_date = pub_date
        self.news_link = news_link
        self.news_description = news_description
        self.img_alt = img_alt
        self.img_src = img_src

    def __repr__(self):
        result = (f"Feed: {self.news_outlett_name}\n\nTitle: {self.news_title}\n"
                  + f"Date: {self.pub_date}\nLink: {self.news_link}\n\n")
        links = f"Links:\n[1]: {self.news_link}\n"
        # add image date if it exists
        if self.img_alt:
            result += f"[image 2: {self.img_alt}][2]"
            links += f"[2]: {self.img_src or 'No link'}\n"
        # add text of article if it exists
        if self.news_description:
            result += f"{self.news_description}\n\n\n"
        result += links + '*'*80

        return result
