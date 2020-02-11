#!/usr/bin/env python
"""
DESCRIPTION

    TODO This describes how to use this script. This docstring
    will be printed by the script if there is an error or
    if the user requests help (-h or --help).

AUTHOR

   Nicholas Hamilton
   nicholas.hamilton@nrel.gov

   Date:
"""

import sys, os, traceback, optparse
import datetime
import numpy as np
import scipy as sp
import pandas as pd

# #------ logging setup --------------------
# import logging
# from logging.config import dictConfig
# logging_config = dict(
#     version=0,
#     formatters={
#         'f': {
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
#         }
#     },
#     handlers={
#         'h': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'f',
#             'level': logging.DEBUG
#         }
#     },
#     root={
#         'handlers': ['h'],
#         'level': logging.DEBUG,
#     },
# )

# dictConfig(logging_config)

# logger = logging.getLogger()
# logger.debug('Locals often make a very good meal of %s', 'visiting tourists')

# #------ logging setup --------------------

from utils import data_logger
# logging setup info
today = datetime.date.today().strftime('%Y%m%d')
log_file = 'tmp_{}.log'.format(today)
log_format = (
    "%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
logger = data_logger('script_log', '../logfiles/{}'.format(log_file))

logger.debug('test')


def main():
    '''
    [summary]

    '''
    global options, args
    # TODO: Do something more interesting here...
    logger.debug('Hello world!')


if __name__ == '__main__':
    main()