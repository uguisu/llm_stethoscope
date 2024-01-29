# coding=utf-8
# author xin.he
import numpy as np
from openai import OpenAI

from llm_stethoscope import AbstractApiTester
from llm_stethoscope.shares.message_code import StandardMessageCode


def connect_server(server_url):
    """
    connect to server
    """
    return OpenAI(
        # This is the default and can be omitted
        # api_key=os.environ.get("OPENAI_API_KEY"),
        api_key='EMPTY',
        base_url=server_url,
    )


class OpenAiApiTester(AbstractApiTester):
    """
    Openai API tester
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

        if self._log_level == 3:
            self._logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                debug_me=f'shape: {self._test_data.shape} | model: {self._model} | server_url: {self._server_url}'
            ))

        client = connect_server(self._server_url)

        # clone an empty array
        infer_array = np.empty(self._test_data.shape, dtype=self._test_data.dtype)

        for i in range(self._test_data.shape[1]):
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": self._test_data[0][i],
                    }
                ],
                model=self._model,
                max_tokens=512,
                temperature=0,
            )

            rst = chat_completion.choices[0].message.content

            # expect value
            infer_array[0][i] = self._test_data[1][i]
            # infer result
            infer_array[1][i] = rst

            if self._log_level == 3:
                self._logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(
                    debug_me=f'🟨 [Confirm 0002]: infer_array[0][{i}] =\n{infer_array[0][i]}'
                             f'🟦 [Confirm 0002]: infer_array[1][{i}] =\n{infer_array[1][i]}'
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
