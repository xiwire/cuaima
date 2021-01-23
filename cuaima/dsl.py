from cuaima.utils import help_text

help_text()
help_text('Welcome to \033[31;7;4m~CUAIMA~\033[0m')
help_text('A live coding language made in python')
help_text('FUN FACT: the cuaima is the second biggest venomous snake in the world')
help_text()

from cuaima.synth import Biast, PutOutStereo
from cuaima.connections import DEFAULT_PORT_MANAGER as _DEFAULT_PORT_MANAGER

show_connections = lambda: _DEFAULT_PORT_MANAGER._connections
