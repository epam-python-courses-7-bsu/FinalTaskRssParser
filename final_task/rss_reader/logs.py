import logging as log
import os


class Logger:
    __verbose = False

    def __init__(self):
        self.logger = self.get_logger()

    def set_stream_logging(self, verbose):
        Logger.__verbose = verbose

    def get_logger(self, name="Unknown"):
        self.logger = log.getLogger(name)
        self.logger.setLevel(log.INFO)
        formatter = log.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

        if Logger.__verbose:
            stream_handler = log.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        file_handler = log.FileHandler(rf"{str(os.getcwd())}\rss_reader\logs\rss_reader.log", 'w')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        return self.logger
