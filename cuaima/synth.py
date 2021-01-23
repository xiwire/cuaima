import random
from cuaima import utils, server


SYNTH_NEW = '/s_new'
SYNTH_FREE = '/s_free'


class BaseSynth(server.TalksToServerMixin):
    """ Manages SuperCollider synth nodes
    """
    def __init__(self, instrument, server=server.DEFAULT_SERVER, **kwargs):
        super().__init__(server)
        self.node = 1027
        self.instrument = instrument
        self.arg_pairs = kwargs

    def call(self):
        """ Call to init the synth in the server
        """
        message = []
        message.append(self.instrument)
        message.append(-1)
        message.append(4)
        message.append(1000)
        message.extend(utils.arg_pairs_from_dict(self.arg_pairs))
        self.client.send_message(SYNTH_NEW, message)
        utils.help_text(f'[DEBUG] sent message to supercollider: {SYNTH_NEW} {message}')
        self.node += 1

    def free(self):
        """ Free the synth in the server
        """
        # self.client.send_message(sc_addresses.SYNTH_FREE, message)
        self.client.send_message(SYNTH_FREE, self.node)


class InstantiableSynth(BaseSynth):
    _instrument = None
    _description = None
    def __init__(self, **arg_pairs):
        super().__init__(self._instrument, **arg_pairs)
        utils.help_text(self._make_banner_text())

    def play(self):
        """ shortcut to call
        """
        self.call()

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


class Yuno(InstantiableSynth):
    _instrument = 'yuno'
    _description = 'A not-so-forgotten relic of the past'
