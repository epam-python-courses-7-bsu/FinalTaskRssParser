from dataclasses import dataclass


@dataclass
class rss_item:
    '''
    Represents a single news from RSS channel
    '''
    title: str
    published: str
    link: str
    media: str

    def format_data(self, data):
        '''
        Method replaces ASCII codes by their char representations 
        '''
        data = data.replace('&#60;', '<')
        data = data.replace('&#x3c;', '<')
        data = data.replace('&#x3C;', '<')
        data = data.replace('&#62;', '>')
        data = data.replace('&#x3e;', '>')
        data = data.replace('&#x3E;', '>')
        data = data.replace('&#38;', '&')
        data = data.replace('&#x26;', '&')
        data = data.replace('&#34;', '"')
        data = data.replace('&#x22;', '"')
        data = data.replace('&#39;', '\'')
        data = data.replace('&#x27;', '\'')
        return data

    def __str__(self):
        self.title = self.format_data(self.title)
        self.published = self.format_data(self.published)
        self.link = self.format_data(self.link)
        return f'TITLE: {self.title}\
            \n\t|| PUBLISHED: {self.published} \
            \n\t|| LINK: {self.link}\
            \n\t|| MEDIA: {self.media}'
