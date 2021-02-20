from cuaima import utils
from cuaima.server import DEFAULT_SERVER


N_SET = "/n_set"


def node_set(node: int, server_ = DEFAULT_SERVER, **kwargs):
    """ set a node's parameters manually
    """
    kwargs_list = utils.arg_pairs_from_dict(kwargs)
    server_.client.send_message(N_SET, [node, *kwargs_list])
