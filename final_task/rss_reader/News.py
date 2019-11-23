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
<<<<<<< HEAD
    strDate: str
=======
    strDate: str
>>>>>>> 89c4f8b1295f477501cad9f19c1d2b63db6309a7
