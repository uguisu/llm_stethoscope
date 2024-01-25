# coding=utf-8
# author xin.he

def demo(j_data) -> dict:
    """
    demo
    :param j_data: json data
    :return: a dict
        {
            'user input 1': 'model output 1',
            'user input 2': 'model output 2',
            ...
            'user input n': 'model output n',
        }
    """

    rtn = {}
    for md in j_data:

        _node: list = md.get('conversations')
        _wrk_key = ''
        _wrk_val = ''
        for _node_dict in _node:
            # make sure data type
            assert isinstance(_node_dict, dict)
            if 'human' == _node_dict.get('from'):
                _wrk_key = _node_dict.get('value')
            if 'gpt' == _node_dict.get('from'):
                _wrk_val = _node_dict.get('value')

        rtn[_wrk_key] = _wrk_val

    return rtn
