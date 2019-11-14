"""This module provides conversion of news to JSON format"""

import json
from typing import Any


def convert_json(data: dict) -> dict:
    """This function converts data to JSON"""

    return json.dumps(data)


def print_json(data: dict):
    """This function prints data in JSON"""

    print(json.dumps(data, ensure_ascii=False, indent=4))

