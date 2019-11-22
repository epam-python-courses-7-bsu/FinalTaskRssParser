import logging

from ConsoleArgument import get_console_argument
from Handler import Handler
from Handler import parse_to_json
from ConsoleOut import print_array_of_news
from ConsoleOut import print_array_of_dict
from ConsoleOut import print_json
from RssException import RssException
from WorkWithCache import read_from_file

def main():
    arg = get_console_argument()
    link = arg.link


    if arg.date:
        news = read_from_file(arg.date)
        print_array_of_dict(news)
    else:
        # standart value -1, in handler we  will process and get all the value
        lim = -1
        if arg.version:
            print("version:  1.0")
            return
        if arg.verbose:
            logging.getLogger().setLevel(logging.INFO)
        if arg.limit:
            if arg.limit <= 0:
                raise RssException("Error count news <0")
            lim = arg.limit
        hand = Handler(link, lim)
        news = hand.get_all()
        if len(news) < lim:
            raise RssException("not have this count of news")
        if arg.json:
            arr_json = []
            for i in news:
                arr_json.append(parse_to_json(i))
            print_json(arr_json)
        else:
            print_array_of_news(news)


if __name__ == "__main__":
    try:
        main()
    # except AttributeError:
    #     print("Error no have attribute")
    except RssException as exc:
        print(exc)
