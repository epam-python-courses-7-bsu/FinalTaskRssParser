""" Main module """
from rss_reader import action_functions
from rss_reader import validation_functions
from rss_reader import exceptions


def main():
    # get command line arguments
    com_line_args = action_functions.get_com_line_args()

    logger = action_functions.create_logger(com_line_args)

    if not validation_functions.check_version_arg(com_line_args, logger):
        try:
            validation_functions.check_internet_connection(logger)
            validation_functions.check_url(com_line_args, logger)

            news_collection = action_functions.get_news(com_line_args, logger)
            validation_functions.check_emptiness(news_collection, logger)

            action_functions.print_news(news_collection, com_line_args, logger)
        except exceptions.Error as e:
            print(e)


if __name__ == "__main__":
    main()

