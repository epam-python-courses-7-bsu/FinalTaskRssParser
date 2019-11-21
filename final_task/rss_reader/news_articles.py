from dataclasses import dataclass


@dataclass()
class NewsArticle:
    """Contain data about an article"""
    news_outlett_name: str
    news_title: str
    pub_date: str
    news_link: str
    news_description: str
    img_alt: str = ''
    img_src: str = ''

    def __str__(self):
        result = (f"Feed: {self.news_outlett_name}\n\nTitle: {self.news_title}\n"
                  + f"Date: {self.pub_date}\nLink: {self.news_link}\n\n")
        links = f"Links:\n[1]: {self.news_link}\n"
        # add image data if it exists
        if self.img_alt:
            result += f"[image 2: {self.img_alt}][2]"
            links += f"[2]: {self.img_src or 'No link'}\n"
        # add text of article if it exists
        if self.news_description:
            result += f"{self.news_description}\n\n\n"
        result += links + '*'*80
        return result

    def __key(self):
        return (self.news_outlett_name, self.news_title, self.pub_date,
                self.news_link, self.news_description, self.img_alt, self.img_src)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, NewsArticle):
            return self.__key() == other.__key()
        return NotImplemented
