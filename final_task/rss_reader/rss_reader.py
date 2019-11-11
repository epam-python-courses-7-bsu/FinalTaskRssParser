import argparse
import json
import logging
import items as itms
import parser_rss


def create_arg_parser():
    """ Create and return argument parser.

    :return: argument parser
    :rtype: 'argparse.ArgumentParser'
    """
    arg_parser_ = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')

    arg_parser_.add_argument('source', type=str, help='RSS URL')
    arg_parser_.add_argument('--version', action='store_true', help='Print version info')
    arg_parser_.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    arg_parser_.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    arg_parser_.add_argument('--limit', type=int, default=0, help='Limit news topics if this parameter provided')

    return arg_parser_


arg_parser = create_arg_parser()
args = arg_parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
    itms.log()
    parser_rss.log()

if args.version:
    print('rssreader-v1.0')
else:
    if not args.limit or args.limit > 0:
        try:
            rss_pars = parser_rss.create_feedparser(args.source, args.limit)

            items = itms.get_items_from_feedparser(rss_pars)

        except TypeError as exc:
            logging.error(exc)
        except Exception as exc:
            logging.error(exc)
        else:
            if args.json:
                try:
                    map_of_dict_items = map(lambda item: itms.item_to_dict(item), items)
                except TypeError as err:
                    logging.error(err)
                else:
                    json_structure = {"feed": rss_pars.feed.title, "items": list(map_of_dict_items)}

                    print(json.dumps(json_structure, indent=4))
            else:
                print(f'Feed: {rss_pars.feed.title}')
                itms.print_items(items)

    else:
        logging.error('Incorrect limit value!')
