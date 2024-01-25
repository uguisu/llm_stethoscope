# coding=utf-8
# author xin.he
from typing import Union


class ConfigInfo:

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
        # run accuracy test
        self._test_common_test_accuracy: bool = False
        # input data file
        self._test_common_input_data_file: str = ''
        # data file parsing function name
        self._test_common_file_object_hook: str = ''

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
                'test_accuracy',
                'input_data_file',
                'file_object_hook',
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
    def test_common_test_accuracy(self) -> Union[None, bool]:
        return self._test_common_test_accuracy

    @test_common_test_accuracy.setter
    def test_common_test_accuracy(self, test_accuracy):
        self._test_common_test_accuracy = eval(test_accuracy)

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
