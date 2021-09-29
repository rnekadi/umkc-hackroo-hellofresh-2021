"""
Author :  Raju Nekadi
Description: This file is utility function called get_session to return a valid logging session
"""

import logging


def get_session():
    # create logger
    logger = logging.getLogger('helloFresh')
    logger.setLevel(logging.INFO)

    # create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(asctime)s %(levelname)s: ' + 'Line - ' + '%(lineno)d' + ':' + '%(message)s',
                                  "%Y%m%d%H%M%S")

    # add formatter to handler
    console_handler.setFormatter(formatter)

    # add handlers to loggers
    logger.addHandler(console_handler)

    return logger
