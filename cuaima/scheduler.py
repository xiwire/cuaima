import atexit
import sched
from multiprocessing import Pipe, Process

from time import time, sleep

from cuaima import patterns, supercollider
from cuaima.server import DEFAULT_SERVER
from cuaima.synth import InstantiableSynth


STOP_MESSAGE = 'STOP'

class ReschedulingSet:
    def __init__(self, synth, beat, **kwargs):
        self.synth = synth
        if not isinstance(beat, patterns.Pattern):
            beat = patterns.Lonely(beat)
        self.beat = beat
        self.kwargs = {}
        for k, v in kwargs.items():
            if not isinstance(v, patterns.Pattern):
                self.kwargs[k] = patterns.Lonely(v)
            else:
                self.kwargs[k] = v

    def call(self, scheduler, server):
        kwargs = {k: v.interpret() for k, v in self.kwargs.items()}
        supercollider.node_set(node=self.synth.node, server_=server, **kwargs)
        print(self.beat, self.beat.collection)
        scheduler.enter(priority=0, delay=self.beat.interpret(), action=ReschedulingSet.call,
                        kwargs={'self': self, 'scheduler': scheduler, 'server': server})
        print('entered!')

    def call_and_end(self, scheduler, server):
        kwargs = {k: v.interpret() for k, v in self.kwargs.items()}
        supercollider.node_set(node=self.synth.node, server_=server, **kwargs)


def polling(pipe, scheduler, server):
    """doc
    """
    while True:
        try:
            if pipe.poll(0):
                received = pipe.recv()
                if received == STOP_MESSAGE:
                    break
            scheduler.run(blocking=True)
        except KeyboardInterrupt:
            pass


class Scheduler:
    """ A little interface to Python's sched.scheduler. Used for scheduling
    events to be sent to SuperCollider. Should be realtime.
    TODO: actually test it's realtime lol
    """
    def __init__(self, server):
        self._scheduler = sched.scheduler(time, sleep)
        self.conn, self.child_conn = Pipe()
        self._server = server
        self.process = Process(target=polling, args=(self.child_conn, self._scheduler, server))
        atexit.register(self._stop)
        self._launch()

    def schedule(self, synth: InstantiableSynth, beat: patterns.Pattern, **kwargs):
        """ Schedule an action
        """
        rescheduling_action = ReschedulingSet(synth, beat, **kwargs)
        rescheduling_action.call(self._scheduler, self._server)

    def _launch(self):
        self.process.start()

    def _stop(self):
        self.conn.send(STOP_MESSAGE)
        self.process.join()


DEFAULT_SCHEDULER = Scheduler(server=DEFAULT_SERVER)
