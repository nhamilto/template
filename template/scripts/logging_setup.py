import sys
import datetime

import logging
import logging.config
import logging.handlers

# logging setup info
today = datetime.date.today().strftime('%Y%m%d')
log_file = 'tmp_{}.log'.format(today)

# email info
fromaddr = 'galion.lidar@protonmail.com'
toaddrs = ['galion.lidar@protonmail.com', 'nicholas.hamilton@nrel.gov']
emailsubject = 'testing email handler'
email_pass = 'at6g1s_g'

log_format = (
    "%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
log_level = logging.INFO


class data_logger(logging.Logger):
    '''
    data_logger subclass of logging.Logger() specifically records the relevant information produced during reception of CL51 atmospheric data.
    '''
    import logging

    def __init__(
            self,
            name,
            log_file,
            log_format=None,
            date_format=None,
            log_level='INFO',
    ):
        # provide defualt log_format and date_format strings
        if log_format is None:
            log_format = '%(asctime)s\n%(name)s\n%(levelname)s\n%(funcName)s %(lineno)d\n%(message)s \n'
        if date_format is None:
            date_format = '%Y/%m/%d %H:%M:%S'

        # make parameters accessible as part of the object interface
        self.name = name
        self.log_file = log_file
        self.log_format = log_format
        self.date_format = date_format
        self.log_level = log_level

        # inherit from logging.Logger class
        logging.Logger.__init__(self, name=name)

        # setup formatter
        data_logging_formatter = logging.Formatter(log_format, date_format)

        # setup logging handler
        data_logging_handler = logging.FileHandler(
            log_file,
            mode='a',
        )
        data_logging_handler.setLevel(log_level)
        data_logging_handler.setFormatter(data_logging_formatter)

        # instantiate logger
        self.setLevel(log_level)
        self.addHandler(data_logging_handler)
