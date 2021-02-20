from pprint import pprint

from cuaima import config


def arg_pairs_from_dict(arg_pairs_dict: dict[str, float]) -> list[str]:
    """ Turn a dict of argument pairs into a format suitable for an OSC message
    """
    arg_pairs = []
    for k, v in arg_pairs_dict.items():
        arg_pairs.append(k)
        arg_pairs.append(v)

    return arg_pairs


def help_text(*args, **kwargs):
    """ Prints help text depending on VERBOSE setting
    """
    if config.VERBOSE:
        print(*args, **kwargs)


def debug_message(*args, **kwargs):
    if config.DEBUG:
        print('\033[2m[DEBUG]', *args, '\033[0m', **kwargs)
