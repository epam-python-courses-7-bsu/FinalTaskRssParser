#!rss_virtual_env/bin/python

"""rss-reader.py 4.5

Usage:
    rss_reader.py (-h | --help)      Show help message and exit
    rss_reader.py <rss-url>          Print rss feeds in human-readable format
    rss_reader.py --version          Print version info
    rss_reader.py --json             Print result as JSON in stdout
    rss_reader.py --verbose          Outputs verbose status messages
    rss_reader.py --limit LIMIT      Limit news topics if this parameter provided
    rss_reader.py --date DATE        Take a date in %%Y%%m%%d format. Print cached news, published on this date.
                                     If source argument passed, print only news from this source
    rss_reader.py --to-epub TO_EPUB  Create a book in epub format from internet
                                     source or database. Receive the path where file will be saved
    rss_reader.py --to-html TO_HTML  Create a file in html format from internet
                                     source or database. Receive the path where file will be saved
"""
try:
    import argparse
    import functions.check_func as ch_f
    import functions.process_func as proc_f
    import functions.print_func as print_f
    import classes.exceptions as exc
    from functions.caching import cache_news, get_cached_news
    from functions.convertation import create_epub, create_html
except ModuleNotFoundError as E:
    print(E)
    exit()

def main():
    """Main function that runs the program"""
    try:
        # Create argument parser instance
        parser = argparse.ArgumentParser()

        # Collect command line arguments
        command_line_args = proc_f.get_arguments(parser)

        # If --verbose argument, set logging level to info
        logger = ch_f.check_verbose(command_line_args)

        if command_line_args.date:
            # Collect news from database
            news_collection = get_cached_news(command_line_args, logger)

            if command_line_args.to_epub or command_line_args.to_html:
                if command_line_args.to_epub:
                    # Creates epub book
                    create_epub(command_line_args, news_collection, logger)

                if command_line_args.to_html:
                    # Create html file
                    create_html(command_line_args, news_collection, logger)

            else:
                # Check --json argument, print news in appropriate form
                print_f.print_feeds_from_database(news_collection, command_line_args, logger)

        else:

            # Checking internet connection
            ch_f.check_internet_connection(logger)

            # Parsing the feed
            feed = proc_f.parse_feed(command_line_args, logger)

            # Collect all entries like a news object collection
            news_collection = proc_f.process_feed(command_line_args, feed, logger)

            # Check if news_collection is not empty
            ch_f.check_news_collection(news_collection, logger)

            # Cache news in database
            cache_news(news_collection, logger)

            create_html(command_line_args, news_collection, logger)

            if command_line_args.to_epub or command_line_args.to_html:
                if command_line_args.to_epub:
                    # Creates epub book
                    create_epub(command_line_args, news_collection, logger)

                if command_line_args.to_html:
                    # Create html file
                    create_html(command_line_args, news_collection, logger)

            else:
                # Check --json argument, print news in appropriate form
                print_f.print_feeds(news_collection, command_line_args, logger)

    except (exc.InternetConnectionError, exc.GettingFeedError, exc.UrlError,
            exc.LimitArgumentError, exc.FeedXmlError, exc.ExtractNewsException,
            exc.DirectoryError) as E:
        print(E)
    except KeyboardInterrupt:
        print(" Keyboard interrupt")


if __name__ == '__main__':
    main()
