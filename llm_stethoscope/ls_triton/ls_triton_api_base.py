# coding=utf-8
# author xin.he
import copy

import numpy as np
import requests

from llm_stethoscope import AbstractApiTester
from llm_stethoscope.shares.message_code import StandardMessageCode

# http request body template
# for example:
#     {
#         "text_input": "introduce nvidia's GPU",
#         "max_tokens": 512,
#         "bad_words": "",
#         "stop_words": "",
#         "pad_id": 2,
#         "end_id": 2
#     }
HTTP_REQUEST_BODY_TEMPLATE = {
    "text_input": '<REPLACE_ME>',
    "max_tokens": 512,
    "bad_words": "",
    "stop_words": "",
    "pad_id": 2,
    "end_id": 2
}

# http response body template
# for example
#     {
#         "cum_log_probs": 0.0,
#         "model_name": "ensemble",
#         "model_version": "1",
#         "output_log_probs": [
#             0.0,
#             ...
#             0.0
#         ],
#         "sequence_end": false,
#         "sequence_id": 0,
#         "sequence_start": false,
#         "text_output": "DIGITS is a deep learning framework that allows researchers and developers to easily build and
#             train deep neural networks using NVIDIA GPUs. It includes a variety of pre-built models, allows for easy
#             hyperparameter tuning, and supports a wide range of deep learning tasks.\n\nDIGITS is built on top of
#             TensorFlow and PyTorch, and can be used with any NVIDIA GPU. It includes a variety of pre-built models,
#             allows for easy hyperparameter tuning, and supports a wide range of deep learning tasks.\n\nYou can learn
#             more about DIGITS here: https://developer.nvidia.com/digits"
#     }


class TritonApiTester(AbstractApiTester):
    """
    Triton API tester
    """
    def __init__(self,
                 test_data,
                 model,
                 server_url,
                 log_level,
                 logger):
        """
        init

        :param test_data: numpy array, shape = [row, group_size]
        :param model: remote model name
        :param server_url: server url
        :param log_level: log level
        :param logger: logger
        """
        super().__init__(test_data, model, server_url, log_level, logger)

    def post_req(self) -> list:
        """
        post request
        :return:
        """

        # init
        self._api_response_list.clear()

        if self._log_level == 3:
            self._logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                debug_me=f'shape: {self._test_data.shape} | model: {self._model} | server_url: {self._server_url}'
            ))

        for i in range(self._test_data.shape[1]):

            # prepare post data
            wrk_post_data = copy.deepcopy(HTTP_REQUEST_BODY_TEMPLATE)['text_input'] = self._test_data[0][i]

            wrk_req = requests.post(f'{self._server_url}', data=wrk_post_data)
            rst = eval(wrk_req.text)

            # make sure return value can be converted
            assert isinstance(rst, dict) and rst.get('text_output') is not None

            # fetch response value
            rst = rst.get('text_output')
            self._api_response_list.append(rst)

        return self._api_response_list
