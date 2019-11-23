#!/usr/bin/env python3.8

import logging


# Create a logger for tracking events that happen when program runs
fileHandler = logging.FileHandler("event_tracker.log", "w", encoding="utf-8")

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG,
                    handlers=[fileHandler])

LOGGER = logging.getLogger("RSS_reader events tracker")
