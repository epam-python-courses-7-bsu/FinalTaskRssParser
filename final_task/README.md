This rss-reader uses requests library to get requests from news websites.
BeautifulSoup from bs4 library enables to find all "items" (pieces of news) from rss feed.
The components of news are devided into groups (title, description, image, link) using dictionary.
News are converted into JSON format using json library method "dump".  
Example of JSON format: {"title": "Germany Has Been Unified for 30 Years. Its Identity Still Is Not.", "date": "Fri, 08 Nov 2019 11:35:06 +0000", "description": "East Germans, bio-Germans, passport Germans: In an increasingly diverse country, the legacy of a divided history has left many feeling like strangers in their own land.", "link": "https://www.nytimes.com/2019/11/08/world/europe/germany-identity.html?emc=rss&partner=rss", "image": "https://static01.nyt.com/images/2019/11/05/world/xxgermany-identity-promo/xxgermany-identity27-moth-v2.jpg"}
