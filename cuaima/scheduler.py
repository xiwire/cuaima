from functools import partial


class Scheduler:
    def __init__(self):
        self._schedule = []

    def schedule(self, target: str, parameters: dict[str, str] = None, time: float = 0.5):
        """ Schedule an OSC message to be sent
        """
        parameters = parameters or {}
        self._schedule.append([(target, parameters, time)])

_DefaultScheduler = Scheduler()


sched = partial(Scheduler.schedule, _DefaultScheduler)
