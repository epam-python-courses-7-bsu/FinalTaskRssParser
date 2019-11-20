#!/usr/bin/env python3.8

from os import path

from jinja2 import Environment, FileSystemLoader


def output_txt_news(all_news, logger):
    """
    Print result in a human readable format (filling the prepared)
    """
    logger.info('Load the template.')

    directory = path.abspath(path.dirname(__file__))
    file_loader = FileSystemLoader((directory + '/templates/'), followlinks=True)
    env = Environment(loader=file_loader)
    template = env.get_template('template.txt')

    logger.info('Fill the template with relevant data.')

    output = template.render(
        all_news=all_news,
    )

    print(output)
