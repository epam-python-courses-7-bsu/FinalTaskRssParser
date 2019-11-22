import os
import FinalTaskRssParser.final_task.rss_reader.CLI as CLI
from FinalTaskRssParser.final_task.rss_reader.rss_parser import rss_handler
from FinalTaskRssParser.final_task.rss_reader.logs import Logger
from FinalTaskRssParser.final_task.rss_reader.data.rss_data_handler import RSSDataHandler
from FinalTaskRssParser.final_task.rss_reader.output_handler.output import OutputHandler


def main():
    """Start point of the program"""

    # Parse arguments from command line
    cl_args = CLI.parse()

    # Prints version of rss_reader and directory where it's placed
    if cl_args.get('version'):
        print(f"\nRSS-Reader {version}" + " from " + str(os.getcwd()))

    # Allow logger to print logs to command-line
    Logger().set_stream_logging(cl_args.get('verbose'))

    # Create logger by implemented function
    logger = Logger().get_logger("rss_reader")

    data = RSSDataHandler(*rss_handler(cl_args.get('source')), cl_args.get('json'), cl_args.get('limit'))

    if not cl_args.get('json'):
        output = OutputHandler(data)
        for text in output.to_readable():
            print(text)
    else:
        print(data.json_data)


if __name__ == '__main__':
    version = '0.1'     # Version of the program
    main()
