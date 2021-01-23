import sched
from multiprocessing import Pipe, Process

from time import time, sleep

from cuaima.synth import InstantiableSynth


def rescheduling_action(f, delay, scheduler, delay_func=None, *args, **kwargs):
    """ TODO: implement delayfunc → a function that can be called to get next time
    """
    def _f():
        f(*args, **kwargs)
        scheduler.schedule(delay=delay, priority=0, action=f, args=args, kwargs=kwargs)
    return _f


class Scheduler:
    """ A little interface to Python's sched.scheduler. Used for scheduling
    events to be sent to SuperCollider. Should be realtime.
    TODO: actually test it's realtime lol
    """
    def __init__(self):
        self._scheduler = sched.scheduler(time, sleep)
        self.conn, self.child_conn = Pipe()
        self._launch()

    def schedule(self, synth: InstantiableSynth, **kwargs):
        """ Schedule an action
        """
        # schedulable_action = rescheduling_action(target.play, 1, self._scheduler, **kwargs)
        # self._scheduler.enter(delay=1, priority=0, action=schedulable_action)

        self.conn.send(dict(delay=1, priority=0, synth=synth.name))

    def _launch(self):
        p = Process(target=self._polling, args=(self.child_conn, self._scheduler))
        p.start()

    def _polling(self, pipe, scheduler):
        while 1:
            if pipe.poll(0):
                received = pipe.recv()
                # I have to do it this way since Synth instances can't be
                # pickled. Maybe in a future rewrite of Synth this can change
                synth_name = received.pop('synth')
                print(synth_name)
                synth_instance = InstantiableSynth.get_by_name(synth_name)
                scheduler.enter(action=synth_instance.play, **received)
            scheduler.run(blocking=False)


DEFAULT_SCHEDULER = Scheduler()
