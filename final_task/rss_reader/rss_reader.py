import argparse
import json_date_util as util
import text_work_util as dt


def parsed():

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("source", nargs='?',  help="RSS URL")
    parser.add_argument("--version", action="store_true", help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided",)

    args = parser.parse_args()

    return args


def main_func():
    limit = parsed().limit

    if parsed().version:
        version = '2.2'
        print('Version: ' + version)

    if parsed().verbose:
        dt.logging.basicConfig(stream=sys.stdout, level=dt.logging.INFO)

    if parsed().source:

        if parsed().limit:
            dict_with_info, all_info = dt.parse_info(parsed().source)

            dict_with_info, limit = dt.fill_dict_with_info(dict_with_info, all_info, limit)

        else:
            dict_with_info, all_info = dt.parse_info(parsed().source)
            dict_with_info, limit = dt.fill_dict_with_info(dict_with_info, all_info, limit)

        dt.calling_func(dict_with_info)

        if parsed().json:
            json_date = util.json_convert(dict_with_info, limit)
            print(json_date)
        else:
            dt.news_output(dict_with_info, limit)
    else:
        print('Input URL')


if __name__ == '__main__':
    main_func()

