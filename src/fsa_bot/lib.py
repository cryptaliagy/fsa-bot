# -*- coding: utf-8 -*-
import logging

from typing import (
    Dict,
    List
)


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
# handler = logging.FileHandler(
#     filename='discord.log',
#     encoding='utf-8',
#     mode='w'
# )
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
))
logger.addHandler(handler)


def csv_string_to_dicts(
    string: str
) -> List[Dict[str, str]]:
    '''
    Converts csv string separated by spaces to a
    list of dictionaries of trigger, source, target
    '''
    items = string.split()
    output = []
    for item in items:
        trigger, source, target = item.split(',')
        output.append({
            'trigger': trigger,
            'source': source,
            'target': target
        })

    return output


def keyval_to_dict(*args: str) -> Dict[str, str]:
    output: Dict[str, str] = {}

    for arg in args:
        key, val = arg.split('=')
        output[key] = val

    return output
