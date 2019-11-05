import argparse
from Handler import Handler


def main():
    version = 1.0

    arg_parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    arg_parser.add_argument("source", type=str, help="RSS URL")
    arg_parser.add_argument("--version", action="store_true", help="Print version info")
    arg_parser.add_argument("--json", action="store_true", help=" Print result as JSON in stdout")
    arg_parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    arg_parser.add_argument("--limit", type=int, default=1, help="Limit news topics if this parameter provided")
    arg_parser_args = arg_parser.parse_args()

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
