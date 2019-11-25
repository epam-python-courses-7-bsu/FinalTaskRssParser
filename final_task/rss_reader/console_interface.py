import argparse
import logging


def parse_args():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", help="RSS url")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("--version", action="version", version="Version 1.4.2", help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--date", type=str, help="Print the new from the specified day, YYYYMMDD format")
    parser.add_argument("--to-html", type=str,
                        help="Convert news in html format, need path, where the file will be saved")
    parser.add_argument("--to-pdf", type=str,
                        help="Convert news in pdf format, need path, where the file will be saved")
    args = parser.parse_args()
    return args


def get_args(args):
    source = args.source
    json = False
    date = None
    path = None
    to_html = False
    to_pdf = False
    limit = -1
    if args.limit:
        limit = args.limit
    if args.json:
        json = True
    if args.verbose:
        verbose = True
        logging.basicConfig(level=logging.DEBUG, format='%(process)d-%(levelname)s-%(message)s')
    else:
        logging.basicConfig(filename='app.log', level=logging.DEBUG, filemode='w',
                            format='%(name)s - %(levelname)s - %(message)s')
    if args.date:
        date = args.date
    logging.debug("Check in interface")
    if args.to_html:
        to_html = True
        path = args.to_html
    if args.to_pdf:
        to_pdf = True
        path = args.to_pdf
    return {"url": source,
            "lim": limit,
            "json": json,
            "date": date,
            "path": path,
            "html": to_html,
            "pdf": to_pdf}
