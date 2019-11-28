import logging
import sys


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
