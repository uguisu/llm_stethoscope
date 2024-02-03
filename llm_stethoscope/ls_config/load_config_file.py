# coding=utf-8
# author xin.he
import configparser
import os

from ..ls_config import ApiServerConfigInfo, ConfigInfo
from ..shares.message_code import StandardMessageCode
from ..static_info import CONFIG_FILE_NAME


def load_config_file(args, logger, comm_rank) -> ConfigInfo:
    """
    load config from file

    :param args: system argument variables
    :param logger: logger
    :param comm_rank: process rank
    :return: an instance of ConfigInfo object
    """
    if args.configFile is None:
        config_f = os.path.join(os.path.abspath(os.path.curdir), CONFIG_FILE_NAME)
    else:
        config_f = args.configFile

    # reading file
    print(StandardMessageCode.I_100_9000_200001.get_formatted_msg(file_name=config_f))

    if not os.path.exists(config_f):
        # Can not find config file
        raise FileExistsError(StandardMessageCode.E_100_9000_000001.get_formatted_msg(cfg_file_name=config_f))

    config_file_reader = configparser.ConfigParser()
    config_file_reader.read(config_f)

    # declare ConfigInfo object
    rtn = ConfigInfo()

    # fetch & setup values
    for k in ConfigInfo.section_map().keys():
        for _item in ConfigInfo.section_map()[k]:
            try:
                exec(f'rtn.{k}_{_item} = config_file_reader["{k}"]["{_item}"]')
            except KeyError as e:
                # some values may do not exist
                exec(f'rtn.{k}_{_item} = None')

    # fetch & setup group values
    for _grp in rtn.test_common_groups:

        api_server = ApiServerConfigInfo()
        try:
            api_server.llm_server_type = config_file_reader[_grp]['llm_server_type']
        except KeyError as e:
            # some values may do not exist
            msg = StandardMessageCode.E_100_9000_000003.get_formatted_msg(config_name=f'{_grp}: llm_server_type')

            if 0 == comm_rank:
                # show error only once
                logger.error(msg)

            raise AttributeError(msg)

        try:
            api_server.url = config_file_reader[_grp]['url']
        except KeyError as e:
            # some values may do not exist
            msg = StandardMessageCode.E_100_9000_000003.get_formatted_msg(config_name=f'{_grp}: url')

            if 0 == comm_rank:
                # show error only once
                logger.error(msg)

            raise AttributeError(msg)

        try:
            api_server.model_name = config_file_reader[_grp]['model_name']
        except KeyError as e:
            # some values may do not exist
            msg = StandardMessageCode.E_100_9000_000003.get_formatted_msg(config_name=f'{_grp}: model_name')

            if 0 == comm_rank:
                # show error only once
                logger.error(msg)

            raise AttributeError(msg)

        rtn.test_group_dict[_grp] = api_server

    del config_file_reader

    return rtn


# TODO not sure what to override
# def override_config_via_cli(args, conf_info: ConfigInfo) -> ConfigInfo:
#     """
#     override config info via command line parameter
#
#     :param args: arguments
#     :param conf_info: target ConfigInfo object
#     :return: fixed ConfigInfo object
#     """
#
#     # if args.bindingAddress is not None:
#     #     conf_info.http_binding_address = args.bindingAddress
#     # if args.bindingPort is not None:
#     #     conf_info.http_binding_port = args.bindingPort
#
#
#     return conf_info


def load_config(args, logger, comm_rank) -> ConfigInfo:
    """
    load config

    :param args: system argument variables
    :param logger: logger
    :param comm_rank: process rank
    :return: an instance of ConfigInfo object
    """

    rtn = load_config_file(args, logger, comm_rank)

    # rtn = override_config_via_cli(args, rtn)

    return rtn
