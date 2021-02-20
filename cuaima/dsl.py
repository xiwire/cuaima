from cuaima.utils import help_text
from functools import partial

help_text()
help_text('Welcome to \033[31;7;4m~CUAIMA~\033[0m')
help_text('A live coding language made in python')
help_text('FUN FACT: the cuaima is the second biggest venomous snake in the world')
help_text()

from cuaima.synth import (
    Biast,
    PutOutStereo,
    WhiteNoise,
    Sine,
    SineLFO,
    SquareLFO,
    Matrix,
    VerbFree,
)
from cuaima.connections import DEFAULT_PORT_MANAGER as _DEFAULT_PORT_MANAGER
conns = partial(print, _DEFAULT_PORT_MANAGER._connections)
from cuaima.scheduler import DEFAULT_SCHEDULER as _DEFAULT_SCHEDULER
sched = partial(_DEFAULT_SCHEDULER.schedule)
from cuaima.patterns import *

STDOUT_L=0
STDOUT_R=1
STDOUT=[STDOUT_L, STDOUT_R]
