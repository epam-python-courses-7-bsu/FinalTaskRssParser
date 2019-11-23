import argparse


def get_console_argument():
    arg = argparse.ArgumentParser(description="read command of comamnd-line")
    arg.add_argument("link", nargs='?', type=str, default="", help="Rss URL")
    arg.add_argument('--limit', help="limit news topics if this parameter privided", type=int)
    arg.add_argument('--verbose', help="verbose", action='store_true')
    arg.add_argument('--json', help="print result as json in stdout", action='store_true')
    arg.add_argument('--version', help="print version info", action='store_true')
    arg.add_argument('--date', help="print news from cache for your date",  type=int)
    arg.add_argument('--to_html', help="create html file with news")
    arg.add_argument('--to_pdf', help="create pdf file with news")

    return arg.parse_args()
