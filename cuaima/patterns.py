import random


def seq(*args):
    """ Sequence
    """
    i = 0
    while 1:
        yield args[i]
        i += 1
        i %= len(args)


def rand(*args):
    """ Random
    """
    while 1:
        yield random.choice(args)


def arp(*args):
    """ Arpeggiate
    """
    while 1:
        yield from (seq(*chord) for chord in args)
