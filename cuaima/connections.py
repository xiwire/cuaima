from enum import Enum
from typing import Union

from cuaima import utils


# Arbitrary unused bus
# TODO: query supercollider to get a new bus
STARTING_EMPTY_BUS = 666


class Rate(Enum):
    AUDIO = 'AUDIO'
    CONTROL = 'CONTROL'


class Orientation(Enum):
    IN = 'IN'
    OUT = 'OUT'


class PortManager:
    _ports: set['Port']
    _connections: set[tuple['Port', 'Port']]

    def __init__(self):
        self._ports = set()
        self._connections = set()
        self._last_empty_bus = STARTING_EMPTY_BUS

    def register(self, port: 'Port'):
        """ Register a new port
        """
        self._ports.add(port)

    def connect(self, port_a: 'Port', port_b: 'Port'):
        """ Connect two ports
        """
        if port_a.rate != port_b.rate:
            raise ValueError('the ports to connect have different rates')
        if port_a.orientation == port_b.orientation:
            raise ValueError('the ports to connect have the same orientation')

        if (port_b, port_a) not in self._connections:
            self._connections.add((self._last_empty_bus, port_a, port_b))
            utils.debug_message(f'CONNECTED PORTS {port_a} AND {port_b} ON BUS {self._last_empty_bus}')
            self._last_empty_bus += 1


DEFAULT_PORT_MANAGER = PortManager()


class Port:
    rate: Rate
    manager: PortManager

    def __init__(
            self,
            name: str,
            module: 'Synth',
            orientation: Union[Orientation, str],
            rate: Union[Rate, str],
            manager: PortManager = DEFAULT_PORT_MANAGER):
        try:
            self.orientation = Orientation(orientation)
        except ValueError as exc:
            raise ValueError('orientation must be one of ("IN", "OUT")') from exc
        try:
            self.rate = Rate(rate)
        except ValueError as exc:
            raise ValueError('rate must be one of ("AUDIO", "CONTROL")') from exc
        self.name = name
        self.module = module
        self.manager = manager
        self.manager.register(self)

    def __gt__(self, other_port):
        self.manager.connect(self, other_port)

    def __lt__(self, other_port):
        self.manager.connect(self, other_port)

    def __repr__(self):
        return f'PORT ({self.name} {self.module} {self.rate.value} {self.orientation.value})'
