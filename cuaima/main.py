import random
from collections import namedtuple
from functools import partial
from typing import Dict, List

from pythonosc import udp_client


Action = namedtuple('Action', ['target', 'parameters', 'time'])


class Server:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def generate_client(self):
        """ Returns a client to the server
        """
        return udp_client.SimpleUDPClient(self.address, self.port)


DEFAULT_SERVER_ADDRESS = 'localhost'
DEFAULT_SERVER_PORT = 57110

DEFAULT_SERVER = Server(DEFAULT_SERVER_ADDRESS, DEFAULT_SERVER_PORT)


class Scheduler:
    def __init__(self):
        self._schedule = []

    def schedule(self, target: str, parameters: dict[str, str] = None, time: float = 0.5):
        """ Schedule an OSC message to be sent
        """
        parameters = parameters or {}
        self._schedule.append(Action(target, parameters, time))

_DefaultScheduler = Scheduler()

sched = partial(Scheduler.schedule, _DefaultScheduler)


class TalksToServerMixin:
    """ Mixin for classes that talk to the server
    """
    def __init__(self, server):
        self.server = server
        self._client = None

    @property
    def client(self):
        """ Returns a suitable client to talk to the server
        """
        if self._client is None:
            self._client = self.server.generate_client()
        # TODO: handle reconnections maybe
        return self._client


SYNTH_NEW = '/s_new'
SYNTH_FREE = '/s_free'


def format_arg_pairs_from_dict(arg_pairs_dict: Dict[str, float]) -> List[str]:
    """ Turn a dict of argument pairs into a format suitable for an OSC message
    """
    arg_pairs = []
    for k, v in arg_pairs_dict.items():
        arg_pairs.append(k)
        arg_pairs.append(v)

    return arg_pairs


class Synth(TalksToServerMixin):
    """ Manages SuperCollider synth nodes
    """
    def __init__(self, instrument, server=DEFAULT_SERVER, **kwargs):
        super().__init__(server)
        self.node = None
        self.instrument = instrument
        self.arg_pairs = kwargs

    def call(self):
        """ Call to init the synth in the server
        """
        message = []
        message.append(self.instrument)
        message.append(-1)
        message.append(4)
        message.append(-1)
        message.extend(format_arg_pairs_from_dict(self.arg_pairs))
        self.client.send_message(SYNTH_NEW, message)

    def free(self):
        """ Free the synth in the server
        """
        # self.client.send_message(sc_addresses.SYNTH_FREE, message)
        self.client.send_message(SYNTH_FREE, self.node)


# Utils
def seq(*args):
    """doc
    """
    i = 0
    while 1:
        yield args[i]
        i += 1
        i %= len(args)


def rand(*args):
    """doc
    """
    while 1:
        yield random.choice(args)
