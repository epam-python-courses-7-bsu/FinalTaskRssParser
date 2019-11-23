import argparse


# temp
__version__ = "0.1"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", action="version", version=f"{parser.prog}s {__version__}",
                        help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("-v", "--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")

    args = parser.parse_args()

    rss_url = args.source

    if args.verbose:
        print("verbosity turned on")

    limit = args.limit if args.limit is not None else 0
