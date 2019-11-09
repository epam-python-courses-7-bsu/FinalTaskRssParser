""" Main module """
import models
import action_functions
import validation_functions

# get command line arguments
com_line_args = models.ArgReader()

logger = action_functions.create_logger(com_line_args)

validation_functions.check_version_arg(com_line_args, logger)
validation_functions.check_internet_connection(com_line_args, logger)
validation_functions.check_url(com_line_args, logger)

news_collection = action_functions.get_news(com_line_args, logger)
validation_functions.check_emptiness(news_collection, logger)

action_functions.print_news(news_collection, com_line_args, logger)

