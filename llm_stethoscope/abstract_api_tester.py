# coding=utf-8
# author xin.he
import numpy as np

from llm_stethoscope.shares.message_code import StandardMessageCode


class AbstractApiTester:
    """
    abstract API tester class
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
        self._test_data = test_data
        self._model = model
        self._server_url = server_url
        self._log_level = log_level
        self._logger = logger
        self._api_response_list = []

    def post_req(self) -> list:
        """
        post request
        :return: model response result as list
        """

        # this method should be overwritten before execute
        raise NotImplementedError()

    def calculate_accuracy(self) -> list:
        """
        calculate accuracy
        :return: accuracy array.
            0 : diff
            1 : same
        """

        # clone an empty array
        infer_array = np.empty(self._test_data.shape, dtype=self._test_data.dtype)

        # expect value
        infer_array[0] = self._test_data[1]
        # infer result
        infer_array[1] = self._api_response_list

        if self._log_level == 3:
            self._logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                debug_me=f'\n'
                         f'🟨 [Confirm 0002]: infer_array[0][0] =\n🔸🔸🔸{infer_array[0][0]}'
                         f'\n'
                         f'🟦 [Confirm 0002]: infer_array[1][0] =\n🔹🔹🔹{infer_array[1][0]}'
            ))

        infer_result = (infer_array[0] == infer_array[1])
        assert isinstance(infer_result, np.ndarray)
        infer_result = infer_result.astype(int)

        if self._log_level == 3:
            self._logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                debug_me=f'[Confirm 0007]: infer_result =\n{infer_result}'
            ))

        # GC
        del infer_array

        return list(infer_result)


def api_tester_factory(llm_server_type: str,
                       test_data,
                       model,
                       server_url,
                       log_level,
                       logger):

    if 'openai' == llm_server_type:
        from llm_stethoscope.ls_openai import OpenAiApiTester
        return OpenAiApiTester(test_data, model, server_url, log_level, logger)

    if 'triton' == llm_server_type:
        from llm_stethoscope.ls_triton import TritonApiTester
        return TritonApiTester(test_data, model, server_url, log_level, logger)

    # unknown server model
    raise ValueError(StandardMessageCode.E_100_9000_000004.get_formatted_msg(model_name=llm_server_type))
