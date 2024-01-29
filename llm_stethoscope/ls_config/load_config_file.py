# coding=utf-8
# author xin.he
import configparser
import os

from ..ls_config import ConfigInfo
from ..shares.message_code import StandardMessageCode
from ..static_info import CONFIG_FILE_NAME


def load_config_file(args) -> ConfigInfo:
    """
    load config from file

    :param args: system argument variables
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
    for i in range(rtn.test_common_group_number - 1):
        try:
            # test_group_{i}_llm_server_type
            exec(f'rtn.test_group_dict["test_group_{i}_llm_server_type"] = '
                 f'config_file_reader["test_group_{i}"]["llm_server_type"]')
            # test_group_{0}_url
            exec(f'rtn.test_group_dict["test_group_{i}_url"] = '
                 f'config_file_reader["test_group_{i}"]["url"]')
        except KeyError as e:
            # some values may do not exist
            raise AttributeError(StandardMessageCode.E_100_9000_000003.get_formatted_msg(config_name=f'test_group_{i}'))

    del config_file_reader

    return rtn


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


def load_config(args) -> ConfigInfo:
    """
    load config

    :param args: system argument variables
    :return: an instance of ConfigInfo object
    """

    rtn = load_config_file(args)

    # rtn = override_config_via_cli(args, rtn)

    return rtn
