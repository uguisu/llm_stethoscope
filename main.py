# coding=utf-8
# author xin.he
import copy
import logging
import mpi4py.MPI as MPI

import llm_stethoscope.shares as shares
from llm_stethoscope.ls_config import load_config, args
from llm_stethoscope import static_info, MPIFileHandler
from llm_stethoscope.shares.message_code import StandardMessageCode

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
config_info_entity = load_config(args, logger, comm_rank)

# pre-load
if comm_rank == 0:
    # show logo
    shares.show_logo()
    # make sure packages
    shares.make_sure_packages(config_info_entity)

    # verify world size
    if 1 == comm_size:
        logger.warning(StandardMessageCode.W_100_9000_100001.get_msg())


# ============================================================
# main process
# NOTICE: DO NOT MOVE FOLLOWING 'IMPORT' CODE TO THE TOP
# ============================================================
import time

from llm_stethoscope import (
    load_data,
    share_with_all_process,
    overwrite_ground_truth,
    api_tester_factory,
    AbstractApiTester,
)


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

        if not config_info_entity.test_common_is_use_annotated_data_as_gt:
            # ignore annotated data, overwrite "ground truth" via special test group
            wrk_new_data = overwrite_ground_truth(config_info_entity.test_group_dict[
                                                      config_info_entity.test_common_groups[0]],
                                                  all_test_data_as_numpy_array,
                                                  config_info_entity.log_level,
                                                  logger)
            # delete old data object
            del all_test_data_as_numpy_array
            # replace
            all_test_data_as_numpy_array = wrk_new_data

    # TODO
    # if comm_rank == 0 and is_performance_test:
    #     # start remote probe
    #     start_remote_probe(str(probe_host), int(ssh_port), str(ssh_username), str(ssh_pwd))

    # split & share data with other process
    _recv_data = share_with_all_process(all_test_data_as_numpy_array,
                                        comm,
                                        config_info_entity.log_level,
                                        logger)

    # stop time
    end_ts = time.perf_counter()

    if config_info_entity.log_level >= 1:
        logger.info(f'Total process time: {end_ts - start_ts} s')

    return _recv_data


if __name__ == '__main__':

    # init
    # - load data
    # - split dataset to all process
    # - TODO start remote probe
    recv_data = init_env()

    test_grp_array = list(copy.deepcopy(config_info_entity.test_common_groups))
    if not config_info_entity.test_common_is_use_annotated_data_as_gt:
        # remove the first group info
        test_grp_array.pop(0)

    # post request
    process_infer_result = []

    for grp_name in test_grp_array:

        if comm_rank > 0:
            from llm_stethoscope.ls_config import ApiServerConfigInfo
            # fetch tester config
            _tester_info = config_info_entity.test_group_dict.get(grp_name)

            assert isinstance(_tester_info, ApiServerConfigInfo)

            # generate api tester
            grp_tester: AbstractApiTester = api_tester_factory(_tester_info.llm_server_type,
                                                               recv_data,
                                                               _tester_info.model_name,
                                                               _tester_info.url,
                                                               config_info_entity.log_level,
                                                               logger)
            # post then get original infer result
            _ = grp_tester.post_req()
            process_infer_result = grp_tester.calculate_accuracy()

        # 'gather' function will return a 2D array, that each process will return a single array,
        # 'all_result' just tie them all
        all_result = comm.gather(process_infer_result, root=0)

        # GC
        process_infer_result.clear()

        if comm_rank == 0:
            flatten_array = []
            for _wrk_array in all_result:
                flatten_array.extend(_wrk_array)

            # GC
            del all_result

            # debug
            if 3 == config_info_entity.log_level:
                for _debug in flatten_array[0:3]:
                    logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                        debug_me=f'flatten_array[0:3] = {_debug}'
                    ))

            # accuracy
            accu = sum(flatten_array) / len(flatten_array)

            max_row_width = 120

            logger.info((f'=== Report [{grp_name}] ' + '=' * max_row_width)[:max_row_width])
            logger.info(f'🎯 Accuracy : {accu}')
            # logger.info(f'Total process time: {end_ts - start_ts} s')
            # logger.info(f'Average infer speed(sentence): { len(flatten_array) / (end_ts - start_ts) }')
            # logger.info(f'Average Response Time(ART): { (end_ts - start_ts) / len(flatten_array) }')
            # logger.info('-' * 120)
            # # logger.info(probe_result)
            # logger.info(f'GPU utilization: Max - {probe_result.get("gpu_utilization").get("max")}, '
            #             f'Min - {probe_result.get("gpu_utilization").get("min")}, '
            #             f'Avg - {probe_result.get("gpu_utilization").get("avg")}')
            logger.info('=' * max_row_width)
