#!rss_virtual_env/bin/python

"""rss-reader.py 1.0

Usage:
    rss_reader.py (-h | --help)      Show help message and exit
    rss_reader.py <rss-url>          Print rss feeds in human-readable format
    rss_reader.py --version          Print version info
    rss_reader.py --json             Print result as JSON in stdout
    rss_reader.py --verbose          Outputs verbose status messages
    rss_reader.py --limit LIMIT      Limit news topics if this parameter provided
"""
try:
    import argparse
    import functions.check_func as ch_f
    import functions.process_func as proc_f
    import functions.print_func as print_f
    import classes.exceptions as exc
except ModuleNotFoundError as E:
    print(E)
    exit()
except KeyboardInterrupt:
    print(" KeyboardInterrupt")
    exit()

def main():
    """Main function that runs the program"""
    try:
        # Create argument parser instance
        parser = argparse.ArgumentParser()

        # Collect command line arguments
        command_line_args = proc_f.get_arguments(parser)

        # If --version argument, print version of program
        ch_f.check_version_argument(command_line_args)

        # If --verbose argument, set logging level to info
        logger = ch_f.check_verbose(command_line_args)

        # Checking internet connection
        ch_f.check_internet_connection(logger)

        # Parsing the feed
        feed = proc_f.parse_feed(command_line_args, logger)

        # Collect all entries like a news object collection
        news_collection = proc_f.process_feed(feed, logger)

        # Check if news_collection is not empty
        ch_f.check_news_collection(news_collection, logger)

        # Check --json argument, print news in appropriate form
        print_f.print_feeds(news_collection, command_line_args, logger)

    except (exc.InternetConnectionError, exc.GettingFeedError, exc.UrlError,
            exc.LimitArgumentError, exc.FeedXmlError) as E:
        print(E)
    except exc.VersionPrinted:
        pass
    except KeyboardInterrupt:
        print(" Keyboard interrupt")


if __name__ == '__main__':
    main()
