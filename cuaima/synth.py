from typing import Union, Iterator
import random
from time import time
from hashlib import sha256

from cuaima import config, connections, server, utils


SYNTH_NEW = '/s_new'
SYNTH_FREE = '/s_free'


# TODO: what are u doing this is awful
# when bidirectional OSC is implemented, change this
node_counter = 10000


class BaseSynth:
    """ Manages SuperCollider synth nodes
    """
    def __init__(self, instrument: str, name: str = None):
        self.instrument = instrument
        if name is None:
            hashed_suffix = sha256(str(time()).encode()).hexdigest()[:4]
            name = f'{self.instrument}#{hashed_suffix}'
        self.name = name
        global node_counter
        self.node = node_counter
        node_counter += 1


class InstantiableSynth(BaseSynth):
    _instrument = None
    _description = None

    _ain_args = tuple()
    _aout_args = tuple()
    _cin_args = tuple()
    _cout_args = tuple()
    _normalled_connections = tuple()

    _all_synths_instances = {}

    def __init__(self, name: str = None, server=server.DEFAULT_SERVER):
        super().__init__(self._instrument, name)
        self._build_ports()
        self._all_synths_instances[self.name] = self
        utils.help_text(self._make_banner_text())

        self._server_init(server)

    def _server_init(self, server_=server.DEFAULT_SERVER):
        """ Call to init the synth in the server
        """
        message = []
        message.append(self.instrument)
        message.append(self.node)
        message.append(0)
        message.append(1)
        message.append(['gate', '0'])
        server_.client.send_message(SYNTH_NEW, message)
        utils.debug_message(f'sent message to supercollider: {SYNTH_NEW} {message}')

    def set(self, server_=server.DEFAULT_SERVER, **kwargs):
        """ set a synth parameter manually
        """
        kwargs_list = utils.arg_pairs_from_dict(kwargs)
        server_.client.send_message('/n_set', [self.node, *kwargs_list])

    def _build_ports(self):
        for port in self._ain_args:
            self.__setattr__(
                port,
                connections.Port(port,
                                 self,
                                 orientation=connections.Orientation.IN,
                                 rate=connections.Rate.AUDIO))
        for port in self._aout_args:
            self.__setattr__(
                port,
                connections.Port(port,
                                 self,
                                 orientation=connections.Orientation.OUT,
                                 rate=connections.Rate.AUDIO))
        for port in self._cin_args:
            self.__setattr__(
                port,
                connections.Port(port,
                                 self,
                                 orientation=connections.Orientation.IN,
                                 rate=connections.Rate.CONTROL))
        for port in self._cout_args:
            self.__setattr__(
                port,
                connections.Port(port,
                                 self,
                                 orientation=connections.Orientation.OUT,
                                 rate=connections.Rate.CONTROL))

    def _make_normalled_connections(self):
        """ Makes normalled connections (i.e. preset internal connections)
        """
        raise NotImplementedError

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
    def get_by_name(cls, name) -> "InstantiableSynth":
        """ Gets a synth by its name
        """
        return cls._all_synths_instances.get(name, None)

    @property
    def ports(self):
        d = {
            connections.Rate.CONTROL: { 
                connections.Orientation.IN: self._cin_args,
                connections.Orientation.OUT: self._cout_args,
            },
            connections.Rate.AUDIO: {
                connections.Orientation.IN: self._ain_args,
                connections.Orientation.OUT: self._aout_args,
            },
        }
        if config.VERBOSE:
            utils.help_text(d)
        return d


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
        'out',
    )


class PutOutStereo(InstantiableSynth):
    _instrument = 'putOutStereo'
    _description = 'A stereo output module with built-in compressor and limiter'

    _normalled_connections = ('in_l', 'in_r')

    _ain_args = {
        'in_l',
        'in_r',
    }

    _aout_args = {
        'out',
    }

class WhiteNoise(InstantiableSynth):
    _instrument = 'wnoise'
    _description = '...it\'s white noise, you know what it is'

    _aout_args = {
        'out',
    }


class Sine(InstantiableSynth):
    _instrument = 'sine'
    _description = 'Here we offer only the purest of waveforms'

    _cin_args = {
        'freq',
        'phase',
    }

    _aout_args = {
        'out',
    }


class SineLFO(InstantiableSynth):
    _instrument = 'sineLFO'
    _description = 'slowwwwwwly does it'

    _cin_args = {
        'freq',
        'phase',
        'amp',
    }

    _cout_args = {
        'out',
    }


class SquareLFO(InstantiableSynth):
    _instrument = 'squareLFO'
    _description = 'it\s on and off and on and off and on...'

    _cin_args = {
        'freq',
        'amp',
    }

    _cout_args = {
        'out',
    }


class VerbFree(InstantiableSynth):
    _instrument = 'verbFree'
    _description = 'Giving you some sense of space'

    _cin_args = {
        'mix',
        'room',
        'damp',
    }

    _ain_args = {
        'in_l',
        'in_r',
    }

    _aout_args = {
        'out_l',
        'out_r',
    }


class Matrix(InstantiableSynth):
    _instrument = 'matrixMixer'
    _description = '3x3 matrix mixer for all your matrix mixing needs'

    _cin_args = {
        'send_1_1',
        'send_1_2',
        'send_1_3',
        'send_2_1',
        'send_2_2',
        'send_2_3',
        'send_3_1',
        'send_3_2',
        'send_3_3',
    }

    _ain_args = {
        'in_1',
        'in_2',
        'in_3',
    }

    _aout_args = {
        'out_1',
        'out_2',
        'out_3',
    }
