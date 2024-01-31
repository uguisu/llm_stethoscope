# coding=utf-8
# author xin.he
import json

import mpi4py
import mpi4py.MPI as MPI
import numpy as np

# IMPORT 'file_object_hook' functions
from .file_hook_mapping import *
from .ls_config import ApiServerConfigInfo

from .shares.message_code import StandardMessageCode


def load_data(input_file, file_object_hook, log_level, logger, comm_size):
    """
    load data
    :param input_file: input file with full path
    :param file_object_hook: data analysis method name
    :param log_level: log level
    :param logger: logger
    :param comm_size: process size
    :return: wrapped data as numpy array. shape = 2
        [
            ['user input 1', 'user input 2', ..., 'user input n']
            ['model output 1', 'model output 2', ..., 'model output n']
        ]
    """

    json_cache_array = []
    with open(file=input_file, encoding='utf-8') as f:
        my_dict = json.load(f)
    json_cache_array.extend(my_dict)

    # use hook function to process data
    final_dict = eval(file_object_hook)(json_cache_array)
    # GC
    del json_cache_array

    i = 0
    k_array = []
    v_array = []
    for k in final_dict.keys():
        k_array.append(k)
        v_array.append(final_dict.get(k))
        i += 1
    k_array = np.ascontiguousarray(k_array)
    v_array = np.ascontiguousarray(v_array)
    wrap_array = np.vstack([k_array, v_array])
    # GC
    del final_dict, k_array, v_array

    # debug
    if log_level >= 2:
        logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
            debug_me=f'wrap_array.shape = {wrap_array.shape}'
        ))
    if log_level == 3:
        logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
            debug_me=f'wrap_array[0][0] =\n{wrap_array[0][0]}'
        ))
        logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
            debug_me=f'wrap_array[1][0] =\n{wrap_array[1][0]}'
        ))

    # confirm
    assert comm_size - 1 <= wrap_array.shape[1]

    return wrap_array


def share_with_all_process(all_test_data,
                           comm: mpi4py.MPI.Intracomm,
                           log_level,
                           logger):
    """
    copy test data to all process
    :param all_test_data: wrapped data as numpy array. shape = 2
    :param comm: mpi4py.MPI object
    :param log_level: log level
    :param logger: logger
    :return: numpy array, shape = [row, group_size]
    """

    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()

    # broadcast parameters to all process
    if comm_rank == 0:
        (_r, _c) = all_test_data.shape
        _dtype = all_test_data.dtype
        group_num = comm_size - 1

        # verify
        if group_num <= 0:
            raise RuntimeError(StandardMessageCode.E_100_9000_000002.get_msg())

        group_size = int(_c / group_num + 0.5)
    else:
        _r = None
        _c = None
        _dtype = None
        group_num = None
        group_size = None

    _r = comm.bcast(_r, root=0)
    _c = comm.bcast(_c, root=0)
    _dtype = comm.bcast(_dtype, root=0)
    group_num = comm.bcast(group_num, root=0)
    group_size = comm.bcast(group_size, root=0)

    if log_level == 3 and comm_rank == comm_size - 1:
        # confirm bcast is success
        logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
            debug_me=f'_r = {_r}, _c = {_c}, _dtype = {_dtype}, group_num = {group_num}, group_size = {group_size}'
        ))

    # passing MPI datatypes explicitly
    recv_data = None
    if comm_rank == 0:
        send_data = all_test_data

        for i in range(group_num):
            split_from = i * group_size
            split_to = split_from + group_size

            if i == group_num - 1 and group_num * group_size < _c:
                # the last group
                split_to = _c

            if log_level == 3:
                logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                    debug_me=f'split_from = {split_from}, split_to = {split_to}'
                ))

            _tmp_array = np.ascontiguousarray(send_data[:, split_from: split_to])

            if log_level == 3:
                logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                    debug_me=f'_tmp_array.shape = {_tmp_array.shape}'
                ))

            comm.Send([_tmp_array, MPI.CHARACTER], dest=i + 1, tag=77)
    else:
        if comm_rank == group_num:
            # the last group
            group_size = _c - (group_num - 1) * group_size

            if log_level == 3:
                logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                    debug_me=f'group_size change to {group_size}'
                ))

        recv_data = np.empty([_r, group_size], dtype=_dtype)

        comm.Recv([recv_data, MPI.CHARACTER], source=0, tag=77)

        if log_level == 3:
            logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                debug_me=f'group_size = {group_size}, group_num = {group_num}'
            ))
            logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                debug_me=f'[Receiver]: {recv_data.shape}'
            ))
            logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                debug_me=f'[confirm ground truth overwrite] recv_data[1][0] = {recv_data[1][0]}'
            ))
            print(f'[confirm ground truth overwrite] len recv_data[1][0] = {len(recv_data[1][0])}')

    return recv_data


def overwrite_ground_truth(ground_truth_server_info: ApiServerConfigInfo,
                           np_test_data: np.ndarray,
                           log_level,
                           logger) -> np.ndarray:
    """
    overwrite ground truth data
    :param ground_truth_server_info: ApiServerConfigInfo instance
    :param np_test_data: data as numpy array
    :param log_level: log level
    :param logger: logger
    :return: new test data with the same shape of input variable "np_test_data"
    """

    from .abstract_api_tester import AbstractApiTester, api_tester_factory

    # generate poster via factory
    ground_truth_api_poster: AbstractApiTester = api_tester_factory(
        ground_truth_server_info.llm_server_type,
        np_test_data,
        ground_truth_server_info.model_name,
        ground_truth_server_info.url,
        log_level,
        logger
    )

    # post
    resp = ground_truth_api_poster.post_req()

    if log_level == 3:
        for _resp in resp:
            logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                debug_me=_resp
            ))

    # confirm size
    assert np_test_data.shape[1] == len(resp)

    return np.vstack([np_test_data[0], resp])
