# coding=utf-8
# author xin.he
from typing import Union


class ApiServerConfigInfo:
    """
    api server config info entity
    """

    def __init__(self):
        # LLM server's type. Only "openai" and "triton" are supported currently
        self._llm_server_type: str = ''
        # server url
        self._url: str = ''
        # model name
        self._model_name: str = ''

    @property
    def llm_server_type(self) -> Union[None, str]:
        return self._llm_server_type

    @llm_server_type.setter
    def llm_server_type(self, llm_server_type):
        self._llm_server_type = llm_server_type

    @property
    def url(self) -> Union[None, str]:
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def model_name(self) -> Union[None, str]:
        return self._model_name

    @model_name.setter
    def model_name(self, model_name):
        self._model_name = model_name


class ConfigInfo:
    """
    config info entity
    """

    def __init__(self):
        # [SECTION] dynamic-pip
        # proxy for install python packages dynamically
        self._dynamic_pip_proxy: str = ''
        # install required packages automatically
        self._dynamic_pip_is_auto_install_package: bool = False

        # [SECTION] log
        # log level
        self._log_level: int = 0

        # [SECTION] test common
        # use annotated data as ground truth
        self._test_common_is_use_annotated_data_as_gt: bool = False
        # input data file
        self._test_common_input_data_file: str = ''
        # data file parsing function name
        self._test_common_file_object_hook: str = ''
        # the number of test groups
        self._test_common_group_number: int = 0
        # test group section names
        self._test_common_groups: tuple = ()

        # [SECTION] test group details
        # - key: group name
        # - val: ApiServerConfigInfo instance
        self._test_group_dict: dict = {}

    @staticmethod
    def section_map() -> dict:
        """
        section and items map
        """
        return {
            'dynamic_pip': [
                'proxy',
                'is_auto_install_package',
            ],
            'log': [
                'level',
            ],
            'test_common': [
                'is_use_annotated_data_as_gt',
                'input_data_file',
                'file_object_hook',
                'groups',
            ],
        }

    @property
    def dynamic_pip_proxy(self) -> Union[None, str]:
        return self._dynamic_pip_proxy

    @dynamic_pip_proxy.setter
    def dynamic_pip_proxy(self, dynamic_pip_proxy):
        self._dynamic_pip_proxy = dynamic_pip_proxy

    @property
    def dynamic_pip_is_auto_install_package(self) -> Union[None, bool]:
        return self._dynamic_pip_is_auto_install_package

    @dynamic_pip_is_auto_install_package.setter
    def dynamic_pip_is_auto_install_package(self, dynamic_pip_is_auto_install_package):
        self._dynamic_pip_is_auto_install_package = eval(dynamic_pip_is_auto_install_package)

    @property
    def log_level(self) -> Union[None, int]:
        return self._log_level

    @log_level.setter
    def log_level(self, log_level):
        self._log_level = int(log_level)

    @property
    def test_common_is_use_annotated_data_as_gt(self) -> Union[None, bool]:
        return self._test_common_is_use_annotated_data_as_gt

    @test_common_is_use_annotated_data_as_gt.setter
    def test_common_is_use_annotated_data_as_gt(self, test_common_is_use_annotated_data_as_gt):
        self._test_common_is_use_annotated_data_as_gt = eval(test_common_is_use_annotated_data_as_gt)

    @property
    def test_common_input_data_file(self) -> Union[None, str]:
        return self._test_common_input_data_file

    @test_common_input_data_file.setter
    def test_common_input_data_file(self, input_data_file):
        self._test_common_input_data_file = input_data_file

    @property
    def test_common_file_object_hook(self) -> Union[None, str]:
        return self._test_common_file_object_hook

    @test_common_file_object_hook.setter
    def test_common_file_object_hook(self, file_object_hook):
        self._test_common_file_object_hook = file_object_hook

    @property
    def test_common_groups(self) -> Union[None, tuple]:
        return self._test_common_groups

    @test_common_groups.setter
    def test_common_groups(self, groups):

        _wrk_in = eval(groups)
        if isinstance(_wrk_in, str):
            # python auto convert input to string, need change
            _wrk_in = tuple([_wrk_in])

        self._test_common_groups = _wrk_in

    @property
    def test_group_dict(self) -> Union[None, dict]:
        return self._test_group_dict
