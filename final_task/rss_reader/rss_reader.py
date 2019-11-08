import CLI
from scrapper import Scrapper
import os
import logging as log


def main():
    logger = log.getLogger(__name__)
    logger.setLevel(log.DEBUG)
    stream_handler = log.StreamHandler()
    logger.addHandler(stream_handler)

    pars = CLI.ArgParser()
    cl_args = pars.parse()

    logger.debug(cl_args)

    if cl_args.get('version'):
        print(f"RSS-Reader {version}" + " from " + str(os.getcwd()))

    scrap = Scrapper(cl_args.get('source'), cl_args.get('limit'), cl_args.get('json'))


if __name__ == '__main__':
    version = '0.1'
    main()
