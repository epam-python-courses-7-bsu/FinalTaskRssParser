import os
import sys
import logging
this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(this_dir)
from Handler import Handler
from Logging import logging_decorator
from ConsoleParse import get_arguments_from_console


@logging_decorator
def main():
    arg_parser_args = get_arguments_from_console()
    version = 1.0

    if arg_parser_args.verbose:
        logging.basicConfig(level=logging.INFO)
    if arg_parser_args.limit <= 0:
        arg_parser_args.limit = 1
    handler = Handler(arg_parser_args.source, arg_parser_args.limit, version)
    try:
        if arg_parser_args.version:
            handler.option_version()
        elif arg_parser_args.json:
            handler.option_json()
        else:
            handler.option_default()
    except AttributeError:
        print("Error, failed to get an attribute. Check correctness URL")


if __name__ == "__main__":

    main()
