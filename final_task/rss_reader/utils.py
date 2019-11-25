#!/usr/bin/env python3.8
"""Contains functions for printing the output result and create path to the file with unique name"""

from datetime import datetime
from os import path

from jinja2 import Environment, FileSystemLoader
from termcolor import colored

from logger import LOGGER


def output_txt_news(cmd_args, all_news):
    """
    Print result in a human readable format (filling the prepared)
    """
    LOGGER.info('Load the template.')

    directory = path.abspath(path.dirname(__file__))
    file_loader = FileSystemLoader((directory + '/templates/'), followlinks=True)
    env = Environment(loader=file_loader)

    if cmd_args.colorize:
        env.filters['colorizetext'] = colored
        template = env.get_template('colorized_template.txt')
    else:
        template = env.get_template('template.txt')

    LOGGER.info('Fill the template with relevant data.')

    output = template.render(all_news=all_news)

    print(output)


def create_path_to_file(file_path, file_name):
    """
    Create a PATH to the file with it's unique name: 'date_time_name.format'
    """
    LOGGER.info("Create a PATH to the file with it's unique name: 'date_time_name.format'")
    cur_time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S_')
    file_name = cur_time + file_name
    path_to_file = path.join(file_path, file_name)

    return path_to_file
