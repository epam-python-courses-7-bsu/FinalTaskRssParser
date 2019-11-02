import json
import feedparser
import argparse

version = 1.0


def gen_entries(parsed):
    for entr in parsed.entries:
        yield entr


def print_feed(parsed):
    print("Feed: ", parsed.feed.title, '\n')


def print_entry_title(entry):
    print("Title: ", entry.title)


def print_entry_date(entry):
    print("Date: ", entry.published)


def print_entry_link(entry):
    print("Link: ", entry.link, '\n')


def print_links_entry(entry):
    print("Links:")
    for i, link in enumerate(entry.links):
        print(f'[{i}] ', link["href"])
    print('\n')


def print_entry(entry):
    print_entry_title(entry)
    print_entry_date(entry)
    print_entry_link(entry)
    print(entry.summary, '\n')
    print_links_entry(entry)


def print_entries(parsed):
    for num, entry in enumerate(parsed.entries):
        if num == arg_parser_args.limit:
            break
        parse_html(entry)
        print_entry(entry)


def print_to_json(obj):
    print(json.dumps(obj, indent=2))


def parse_html(entry):
    """selects alt and src attributes from <img> and removes all the html tags from the entry"""
    while entry.summary.count('<img'):
        src = entry.summary[entry.summary.find("src=\"") + len("src=\""):
                            entry.summary.find('"', entry.summary.find("src=\"") + len("src=\""))
              ]
        entry.links.append({"href": src})
        alt = entry.summary[entry.summary.find("alt=\"") + len("alt=\""):
                            entry.summary.find('"', entry.summary.find("alt=\"") + len("alt=\""))
              ]
        start_cut = entry.summary.find("<img")
        entry.summary = entry.summary[: start_cut] \
                        + f"[image {len(entry.links) - 1}: " + alt + "]" \
                        + f"[{len(entry.links) - 1}] " \
                        + entry.summary[entry.summary.find(">", start_cut + len("<img")) + 1:]

    while entry.summary.count('<'):
        entry.summary = entry.summary[:entry.summary.find('<')] + entry.summary[entry.summary.find('>') + 1:]


def convert_to_dict(parsed, entry):
    entry_dict = {
        "Feed": parsed.feed.title,
        "Title": entry.title,
        "Date": entry.published,
        "Link": entry.link,
        "Links": [link["href"] for link in entry.links]
    }
    return entry_dict


"""execution options: json, version, limit ..."""


def case_json():
    parsed = feedparser.parse(arg_parser_args.source)
    gen = gen_entries(parsed)
    for num, entry in enumerate(gen):
        if num == arg_parser_args.limit:
            break
        print_to_json(convert_to_dict(parsed, entry))


def case_default():
        parsed = feedparser.parse(arg_parser_args.source)
        print_feed(parsed)
        print_entries(parsed)


def case_version():
    print("version ", version)


"""arguments from cl"""
arg_parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
arg_parser.add_argument("source", type=str, help="RSS URL")
arg_parser.add_argument("--version", action="store_true", help="Print version info")
arg_parser.add_argument("--json", action="store_true", help=" Print result as JSON in stdout")
arg_parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
arg_parser.add_argument("--limit", type=int, default=1, help="Limit news topics if this parameter provided")
arg_parser_args = arg_parser.parse_args()

try:
    if arg_parser_args.version:
        case_version()
    elif arg_parser_args.json:
        case_json()
    else:
        case_default()
except AttributeError:
    print("Error, failed to get an attribute. Check correctness URL")
