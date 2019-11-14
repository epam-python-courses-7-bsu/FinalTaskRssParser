#!/usr/bin/env python3.8


import logging
import sys


# Create a logger for tracking events that happen when program runs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stdout,
                    level=logging.WARNING)

LOGGER = logging.getLogger("RSS_reader events tracker")
