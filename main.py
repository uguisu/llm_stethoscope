# coding=utf-8
# author xin.he
import logging
import mpi4py.MPI as MPI

import llm_stethoscope.shares as shares
from llm_stethoscope.ls_config import load_config, args
from llm_stethoscope import static_info, MPIFileHandler

# ============================================================
# declare parameter
# ============================================================
# MPI process config
comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

# logger
logger = logging.getLogger("rank[%i]" % comm.rank)
logger.setLevel(logging.INFO)
_log_formatter = logging.Formatter(static_info.LOG_FORMAT_STR)

_file_handler = MPIFileHandler("./stethoscope.log")
_file_handler.setFormatter(_log_formatter)
logger.addHandler(_file_handler)

_console_handler = logging.StreamHandler()
_console_handler.setFormatter(_log_formatter)
logger.addHandler(_console_handler)

# read config
config_info_entity = load_config(args)

# pre-load
if comm_rank == 0:
    # show logo
    shares.show_logo()
    # make sure packages
    shares.make_sure_packages(config_info_entity)


# ============================================================
# main process
# NOTICE: DO NOT MOVE FOLLOWING 'IMPORT' CODE TO THE TOP
# ============================================================
import time

from llm_stethoscope import load_data, share_with_all_process


def init_env():
    """
    init environment
    """

    global logger

    # start time
    start_ts = time.perf_counter()

    # load data
    all_test_data_as_numpy_array = None
    if comm_rank == 0:
        # load data from json file
        all_test_data_as_numpy_array = load_data(config_info_entity.test_common_input_data_file,
                                                 config_info_entity.test_common_file_object_hook,
                                                 config_info_entity.log_level,
                                                 logger,
                                                 comm_size)
    # if comm_rank == 0 and is_performance_test:
    #     # start remote probe
    #     start_remote_probe(str(probe_host), int(ssh_port), str(ssh_username), str(ssh_pwd))

    # split & share data with other process
    recv_data = share_with_all_process(all_test_data_as_numpy_array,
                                       comm,
                                       config_info_entity.log_level,
                                       logger)

    # stop time
    end_ts = time.perf_counter()

    logger.info(f'Total process time: {end_ts - start_ts} s')


if __name__ == '__main__':

    init_env()
