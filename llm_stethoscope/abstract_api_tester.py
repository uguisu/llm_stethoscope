# coding=utf-8
# author xin.he
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

    def post_req(self) -> list:
        """
        post request
        :return: model response result as list
        """

        # this method should be overwritten before execute
        raise NotImplementedError()


def api_tester_factory(llm_server_type: str,
                       test_data,
                       model,
                       server_url,
                       log_level,
                       logger
                       ):

    if 'openai' == llm_server_type:
        from llm_stethoscope.ls_openai import OpenAiApiTester
        return OpenAiApiTester(test_data, model, server_url, log_level, logger)

    if 'triton' == llm_server_type:
        from llm_stethoscope.ls_triton import TritonApiTester
        return TritonApiTester(test_data, model, server_url, log_level, logger)

    # unknown server model
    raise ValueError(StandardMessageCode.E_100_9000_000004.get_formatted_msg(model_name=llm_server_type))
