import logging
import sys

from . import news_parser


# Set basic configs for logging
stdoutHandler = logging.StreamHandler(sys.stdout)
fileHandler = logging.FileHandler("parser.log", "a", encoding="utf-8")
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG,
                    handlers=[fileHandler])


def makeVerbose():
    '''
    1. print logs in stdout if there is --verbose argument
    '''
    stderrLogger = logging.StreamHandler()
    stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    logging.getLogger().addHandler(stderrLogger)


def createLogs(item):
    '''
     1. log news in log file
    '''
    logging.debug("Title: " + str(item.title))
    logging.debug("Date: " + str(item.published))
    logging.debug("Link: " + str(item.link))
    logging.debug("Description: " + news_parser.getDescription(item.description))
    logging.debug("Links:"+"\n[1]: " + str(item.link) +
                "(link)\n[2]: " + str(news_parser.checkMediaContent(item)) + '\n')