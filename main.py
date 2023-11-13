# coding=utf-8
# author xin.he
import logging

import argparse

from llm_stethoscope import shares, static_info

# ============================================================
# declare parameter
# ============================================================
# logger
logger = logging.getLogger('llm_stethoscope')
logger.setLevel(logging.INFO)

# show logo
shares.show_logo()

# make sure packages
shares.make_sure_packages(logger)


# ============================================================
# main process
# NOTICE: DO NOT MOVE FOLLOWING 'IMPORT' CODE TO THE TOP
# ============================================================
def _argparse():
    """
    get input arguments
    :return: argument object
    """
    parser = argparse.ArgumentParser(description="Large Language Model(llm) stethoscope")
    parser.add_argument('--test-acc', action='store_true', dest='test-acc', default=False, help='Run accuracy test')
    parser.add_argument('--debug', action='store_true', dest='is_debug', default=False, help='Debug flag')

    return parser.parse_args()


def init_env():
    """
    init environment
    """

    global logger

    # log file =====
    _log_formatter = logging.Formatter(static_info.LOG_FORMAT_STR)
    _file_handler = logging.FileHandler('my.log', mode='w', encoding='utf-8')
    _file_handler.setFormatter(_log_formatter)
    logger.addHandler(_file_handler)

    _console_handler = logging.StreamHandler()
    _console_handler.setFormatter(_log_formatter)
    logger.addHandler(_console_handler)


if __name__ == '__main__':

    # get arguments
    args = _argparse()

    init_env()

    if args.is_debug:
        pass
