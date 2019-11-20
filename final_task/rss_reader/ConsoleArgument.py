import argparse


def get_console_argument():
    arg = argparse.ArgumentParser(description="read command of comamnd-line")
    arg.add_argument("link", type=str, default="", help="Rss URL")
    arg.add_argument('--limit', help="limit news topics if this parameter privided", type=int)
    arg.add_argument('--verbose', help="verbose", action='store_true')
    arg.add_argument('--json', help="print result as json in stdout", action='store_true')
    arg.add_argument('--version', help="print version info", action='store_true')
    return arg.parse_args()
