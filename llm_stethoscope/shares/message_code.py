# coding=utf-8
# author xin.he
from enum import Enum


class StandardMessageCode(Enum):
    """
    Standard Message Code
    """
    # error
    E_100_9000_000001 = (1009000000001, 'Can not find config file {cfg_file_name}')

    # warning
    # W_100_9000_100001 = (1009000100001, 'The thread pool is full')

    # info
    I_100_9000_200001 = (1009000200001, 'Reading {file_name}')
    # I_100_9000_200002 = (1009000200002, 'Call {method_name}() start')
    # I_100_9000_200003 = (1009000200003, 'Call {method_name}() end')
    I_100_9000_200004 = (1009000200004, '[Confirm -> 🦋] {debug_me}')

    def get_code(self):
        return self.value[0]

    def get_msg(self):
        return self.value[1]

    def get_formatted_msg(self, **info):
        if info:
            msg = self.value[1].format_map(info)
            return '[{code}] {msg}'.format(code=self.value[0], msg=msg)
        return '[{code}] {msg}'.format(code=self.value[0], msg=self.value[1])
