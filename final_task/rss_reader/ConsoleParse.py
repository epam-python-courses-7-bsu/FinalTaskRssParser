import argparse


def get_arguments_from_console():
    arg_parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument("source", nargs='?', type=str, default="", help="RSS URL")
    arg_parser.add_argument("--version", action="store_true", help="Print version info")
    arg_parser.add_argument("--json", action="store_true", help=" Print result as JSON in stdout")
    arg_parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    arg_parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    arg_parser.add_argument("--to-html", type=str, help="Output to html format")
    arg_parser.add_argument("--to-pdf", type=str, help="Output to pdf format")
    group.add_argument("--date", type=int, help="The new from the specified day will be printed out")

    return arg_parser.parse_args()
