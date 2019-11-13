import logging


def turn_on_logging(logger):
    """ Set debug level and set format of logging """
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
