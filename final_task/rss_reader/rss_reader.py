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
    if not (arg_parser_args.source or arg_parser_args.version or arg_parser_args.date or arg_parser_args.json
            or arg_parser_args.to_html or arg_parser_args.to_pdf):
        return
    handler = Handler(arg_parser_args.source, arg_parser_args.limit, version)
    if not arg_parser_args.limit:
        arg_parser_args.limit = len(handler.parsed.entries)
        handler.limit = arg_parser_args.limit
    if arg_parser_args.limit <= 0 and not version:
        raise RSSReaderException("Error. Incorrect value of argument limit")

    if arg_parser_args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    if arg_parser_args.version:
        handler.option_version()
    elif arg_parser_args.date:
        handler.option_date(str(arg_parser_args.date), arg_parser_args.json,
                            arg_parser_args.to_html, arg_parser_args.to_pdf
                            )
    elif arg_parser_args.json:
        handler.option_json()
    else:
        if arg_parser_args.to_html:
            handler.option_html(arg_parser_args.to_html)
        if arg_parser_args.to_pdf:
            handler.option_pdf(arg_parser_args.to_pdf)
    if not (arg_parser_args.version or arg_parser_args.date or arg_parser_args.json
            or arg_parser_args.to_html or arg_parser_args.to_pdf):
        handler.option_default()


if __name__ == "__main__":
    try:
        main()
    except AttributeError:
        print("Error, failed to get an attribute.")
    except PermissionError:
        print("Error, close the file for output of news")
    except RSSReaderException as rss_exc:
        print(rss_exc)