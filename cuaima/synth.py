from typing import Union, Iterator
import random
from time import time
from hashlib import sha256

from cuaima import connections, server, utils


SYNTH_NEW = '/s_new'
SYNTH_FREE = '/s_free'


def interpret_patterns(kwargs: dict[str, Union[float, Iterator]]):
    """ interprets patterns present in dict
    """
    d = {}
    for k, v in kwargs.items():
        try:
            next_value = next(v)
            d[k] = next_value
        except TypeError:  # we check if v is an iterator
            d[k] = v
    return d


class BaseSynth(server.TalksToServerMixin):
    """ Manages SuperCollider synth nodes
    """
    def __init__(self, instrument: str, name: str = None, _server=server.DEFAULT_SERVER):
        super().__init__(_server)
        self.node = 1000
        self.instrument = instrument
        self.name = name or f'{self.instrument}#{sha256(str(time()).encode()).hexdigest()[:4]}'

    def call(self, **kwargs):
        """ Call to init the synth in the server
        """
        message = []
        message.append(self.instrument)
        message.append(self.node)
        message.append(0)
        message.append(1)
        interpreted_kwargs = interpret_patterns(kwargs)
        message.extend(utils.arg_pairs_from_dict(interpreted_kwargs))
        self.client.send_message(SYNTH_NEW, message)
        utils.debug_message(f'sent message to supercollider: {SYNTH_NEW} {message}')
        self.node += 1


class InstantiableSynth(BaseSynth):
    _instrument = None
    _description = None

    _ain_args = tuple()
    _aout_args = tuple()
    _cin_args = tuple()
    _cout_args = tuple()

    _all_synths_instances = {}

    def __init__(self, name: str = None):
        super().__init__(self._instrument, name)
        self._build_ports()
        self._all_synths_instances[self.name] = self
        print(self._all_synths_instances)
        utils.help_text(self._make_banner_text())

    def _build_ports(self):
        for port in self._ain_args:
            self.__setattr__(port, connections.Port(self, orientation='in', rate='a'))
        for port in self._aout_args:
            self.__setattr__(port, connections.Port(self, orientation='out', rate='a'))
        for port in self._cin_args:
            self.__setattr__(port, connections.Port(self, orientation='in', rate='c'))
        for port in self._cout_args:
            self.__setattr__(port, connections.Port(self, orientation='out', rate='c'))

    def play(self, **kwargs):
        """ shortcut to call
        """
        self.call(**kwargs)

    def _make_banner_text(self):
        """ Prints the banner text for a synth
        """
        color = random.choice(range(33,37))
        banner_width = len(self._description)
        start_color = f'\033[{color}m'
        end_color = '\033[0m'
        bold = '\033[1m'

        banner_text = '\n'.join([
            '',
            f'{start_color}=' * banner_width,
            bold + self._instrument.upper().center(banner_width) + end_color + start_color,
            self._description,
            ('=' * banner_width) + end_color,
            ''
        ])

        return banner_text

    @classmethod
    def get_by_name(cls, name):
        """ Gets a synth by its name
        """
        return cls._all_synths_instances.get(name, None)


    def __repr__(self):
        return f'{self.name} ({self.instrument})'


class Biast(InstantiableSynth):
    _instrument = 'biast'
    _description = 'Weird parametrized funky drum machine from hell. Enjoy!'

    _cin_args = (
        'attack',
        'decay',
        'fm',
        'harmonic',
        'spread',
        'penv',
        'fold',
    )
    _aout_args = (
        'out_bus',
    )


class PutOutStereo(InstantiableSynth):
    _instrument = 'putOutStereo'
    _description = 'A stereo output module with built-in compressor and limiter'

    _ain_args = {
        'inBus_l',
        'inBus_r',
    }

    _aout_args = {
        'outBus',
    }
