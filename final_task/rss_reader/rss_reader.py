import logging

from ConsoleArgument import get_console_argument
from Handler import Handler
from Handler import parse_to_json
from ConsoleOut import print_array_of_news
from ConsoleOut import print_array_of_dict
from ConsoleOut import print_json
from RssException import RssException
from WorkWithCache import read_from_file
from ConvertToHtmlAndPdf import create_html_news
from ConvertToHtmlAndPdf import create_pdf_news
from ConvertToHtmlAndPdf import convert_Dict_to_News

def main():
    arg = get_console_argument()
    link = arg.link
    lim = -1

    # if user enter to_html
    if arg.to_html:
        # if user enter link
        if arg.link:
            if arg.limit:
                if arg.limit <= 0:
                    raise RssException("Error count news <0")
                lim = arg.limit

            hand = Handler(link, lim)
            news = hand.get_all()
        # if user enter --date
        elif arg.date:
            if arg.limit:
                lim = arg.limit
            dict_news=read_from_file(arg.date, lim)
            news=convert_Dict_to_News(dict_news)
        else:
            raise RssException("Error. Please enter url or --date")
        create_html_news(arg.to_html, news)

    # if user enter to_pdf
    elif arg.to_pdf:
        # if user enter link
        if arg.link:
            if arg.limit:
                if arg.limit <= 0:
                    raise RssException("Error count news <0")
                lim = arg.limit

            hand = Handler(link, lim)
            news = hand.get_all()
        # if user --date
        elif arg.date:
            if arg.limit:
                lim = arg.limit
            dict_news=read_from_file(arg.date, lim)
            news=convert_Dict_to_News(dict_news)
        else:
            raise RssException("Error. Please enter url or --date")
        create_pdf_news(arg.to_pdf, news)

    elif arg.date:
        if arg.limit:
            lim = arg.limit
        news = read_from_file(arg.date, lim)
        if arg.json:
            print_json(news)
        else:
            print_array_of_dict(news)


    else:
        # standart value -1, in handler we  will process and get all the value

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
    except AttributeError:
         print("Error no have attribute")
    except RssException as exc:
        print(exc)

