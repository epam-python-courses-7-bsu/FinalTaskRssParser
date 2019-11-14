import argparse
import sys
import json_date_util as util
import text_work_util as dt


def parsed():

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("--version", action="store_true", help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided")

    args = parser.parse_args()
    if not args.limit:
        args.limit = 0
    return args


def run():

    if parsed().version:
        version = '1.8'
        print('Version: ' + version)

    if parsed().verbose:
        dt.logging.basicConfig(stream=sys.stdout, level=dt.logging.INFO)

    if parsed().limit:
        dict_with_info = dt.take_info(parsed().source, parsed().limit)
        dt.make_all_text_better(dict_with_info)

        if parsed().json:
            json_date = util.json_convert(dict_with_info, parsed().limit)
            print(json_date)
        else:
            dt.news_output(dict_with_info, parsed().limit)


if __name__ == '__main__':
    run()

