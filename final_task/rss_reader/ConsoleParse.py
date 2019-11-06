import argparse


def get_arguments_from_console():
    arg_parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    arg_parser.add_argument("source", nargs='?', type=str, help="RSS URL")
    arg_parser.add_argument("--version", action="store_true", help="Print version info")
    arg_parser.add_argument("--json", action="store_true", help=" Print result as JSON in stdout")
    arg_parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    arg_parser.add_argument("--limit", type=int, default=700, help="Limit news topics if this parameter provided")

    return arg_parser.parse_args()
