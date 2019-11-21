import os
import sys
import logging

this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(this_dir)
from Handler import Handler
from Logging import logging_decorator
from ConsoleParse import get_arguments_from_console
from RSSReaderException import RSSReaderException


@logging_decorator
def main():
    arg_parser_args = get_arguments_from_console()
    version = 4.0

    handler = Handler(arg_parser_args.source, arg_parser_args.limit, version)
    if not arg_parser_args.limit:
        arg_parser_args.limit = len(handler.parsed.entries)

    if arg_parser_args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    if arg_parser_args.limit <= 0 and arg_parser_args.date is False:
        raise RSSReaderException("Error. Incorrect value of argument limit")

    if arg_parser_args.version:
        handler.option_version()
    elif arg_parser_args.date:
        handler.option_date(str(arg_parser_args.date), arg_parser_args.json,
                            arg_parser_args.to_html, arg_parser_args.to_html,
                            arg_parser_args.to_pdf, arg_parser_args.to_pdf
                            )
    elif arg_parser_args.json:
        handler.option_json()
    elif arg_parser_args.to_html and arg_parser_args.to_pdf:
        handler.option_html(arg_parser_args.to_html)
        handler.option_pdf(arg_parser_args.to_pdf)
    elif arg_parser_args.to_html:
        handler.option_html(arg_parser_args.to_html)
    elif arg_parser_args.to_pdf:
        handler.option_pdf(arg_parser_args.to_pdf)
    else:
        handler.option_default()


if __name__ == "__main__":
    try:
        main()
    except AttributeError:
        print("Error, failed to get an attribute.")
    except RSSReaderException as rss_exc:
        print(rss_exc)
    except IndexError:
        print("Error, enter the correct path")
    except PermissionError:
        print("Error, close the file for output of news")
