""" Main module """
import action_functions
import validation_functions
import exceptions
import caching_functions


def main():
    try:
        # get command line arguments
        com_line_args = action_functions.get_com_line_args()

        logger = action_functions.create_logger(com_line_args)

        if not validation_functions.check_version_arg(com_line_args, logger):
            if com_line_args.date:
                news_collection = caching_functions.get_cached_news(com_line_args, logger)
                action_functions.print_cache_news(news_collection, com_line_args, logger)
            else:
                validation_functions.check_internet_connection(logger)
                validation_functions.check_url(com_line_args, logger)

                news_collection = action_functions.get_news(com_line_args, logger)
                validation_functions.check_emptiness(news_collection, logger)
                caching_functions.cache_news(news_collection, logger)
                action_functions.print_news(news_collection, com_line_args, logger)
    except exceptions.Error as e:
        print(e)


if __name__ == "__main__":
    main()
