import html

def find_description(description) -> str:
    """ Parses description in readable format, return description"""

    text = description
    index_of_text_beginning = description.find(">")
    while index_of_text_beginning != -1:
        if index_of_text_beginning != len(description) - 1:
            if description[index_of_text_beginning + 1] != "<":
                text = description[index_of_text_beginning + 1:]
                text = text[: text.find('<')]
                break
        description = description[index_of_text_beginning + 1:]
        index_of_text_beginning = description.find(">")
    return text

def taking_information_from_feedparser(feed, dict_of_args) -> list:
    """ Creates a list with arguments: title, date, link, description, link of image and description of image, if
    they exist for each news"""

    list_of_args = [dict_of_args.get("url"), html.unescape(feed.get("title", "")),
                    feed.get("published", "")]
    description = feed.get("description", "")
    description_to_put = find_description(description)

    # trying to get link of image and description of image
    index_of_link = description.find("src")
    link_of_img = ""
    if index_of_link != -1:
        link_of_img = description[index_of_link + 5:]
        link_of_img = link_of_img[: link_of_img.find('"')]

        index_of_link = description.find("alt")
        alt_of_img = description[index_of_link + 5:]
        alt_of_img = alt_of_img[: alt_of_img.find('"')]

        description_to_put = "[image: " + alt_of_img + "][2]" + description_to_put
    list_of_args.append(html.unescape(description_to_put))
    list_of_args.append(feed.get("link", ""))
    list_of_args.append(link_of_img)
    return list_of_args

def printing(args):
    """ Just prints news"""

    if args.link_of_img:
        print("Title: %s\nDate: %s\nLink: %s\n\n%s\n\nLinks:\n[1]: %s\n[2]: %s" %
              (args.title, args.date, args.link, args.description, args.link, args.link_of_img))
    else:
        print("Title: %s\nDate: %s\nLink: %s\n\n%s\n\nLinks:\n[1]: %s" %
              (args.title, args.date, args.link, args.description, args.link))
    print("__________________________________________________________________")

class InfoAboutNews():

    def __init__(self, list_of_args):
        self.feed = list_of_args[0]
        self.title = list_of_args[1]
        self.date = list_of_args[2]
        self.description = list_of_args[3]
        self.link = list_of_args[4]
        self.link_of_img = list_of_args[5]