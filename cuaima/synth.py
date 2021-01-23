import itertools
import random

from cuaima import connections, server, utils


SYNTH_NEW = '/s_new'
SYNTH_FREE = '/s_free'


class BaseSynth(server.TalksToServerMixin):
    """ Manages SuperCollider synth nodes
    """
    def __init__(self, instrument, _server=server.DEFAULT_SERVER):
        super().__init__(_server)
        self.node = 1000
        self.instrument = instrument

    def call(self, **kwargs):
        """ Call to init the synth in the server
        """
        message = []
        message.append(self.instrument)
        message.append(self.node)
        message.append(0)
        message.append(1)
        message.extend(utils.arg_pairs_from_dict(kwargs))
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

    def __init__(self, **arg_pairs):
        super().__init__(self._instrument, **arg_pairs)
        self._build_ports()
        utils.help_text(self._make_banner_text())

    def _build_ports(self):
        for port in self._ain_args:
            self.__setattr__(port, connections.Port(orientation='in', rate='a'))
        for port in self._aout_args:
            self.__setattr__(port, connections.Port(orientation='out', rate='a'))
        for port in self._cin_args:
            self.__setattr__(port, connections.Port(orientation='in', rate='c'))
        for port in self._cout_args:
            self.__setattr__(port, connections.Port(orientation='out', rate='c'))

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
