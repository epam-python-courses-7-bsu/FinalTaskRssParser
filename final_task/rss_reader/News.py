from dataclasses import dataclass

''' in this class, we store news in the required format and 
    implement all the logic for processing news in the class Handler
'''


@dataclass
class News:
    news: str
    link: str
    title: str
    date: str
    links: []
    strDate: str