from enum import Enum
from typing import Union

from cuaima import server, utils


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

    def __init__(self, server: server.Server = server.DEFAULT_SERVER):
        self._ports = set()
        self._connections = set()
        self._last_empty_bus = STARTING_EMPTY_BUS
        self._server = server

    def register(self, port: 'Port'):
        """ Register a new port
        """
        self._ports.add(port)

    def connect(self, out_port: 'Port', in_port: 'Port'):
        """ Connect two ports
        """
        if in_port.rate != out_port.rate:
            raise ValueError('the ports to connect have different rates')
        if in_port.orientation == out_port.orientation:
            raise ValueError('the ports to connect have the same orientation')
        if out_port.orientation == Orientation.IN:
            in_port, out_port = out_port, in_port

        if (in_port, out_port) not in self._connections:
            connection_t = (in_port, out_port)
            self._connections.add(connection_t)
            utils.debug_message(f'CONNECTED {out_port} TO {in_port} ON BUS {self._last_empty_bus}')
            if in_port.rate == Rate.CONTROL:
                self._server_connect_control_port(in_port, out_port, self._last_empty_bus)
            else:
                self._server_connect_audio_port(in_port, out_port, self._last_empty_bus)
            self._last_empty_bus += 1

    def _server_connect_control_port(self, in_port, out_port, bus_index):
        client = self._server.client
        # we set the out port to the bus
        client.send_message('/n_set', [out_port.module.node, out_port.name, bus_index])
        # and we map the in port's value to that bus
        client.send_message('/n_map', [in_port.module.node, in_port.name, bus_index])

    def _server_connect_audio_port(self, in_port, out_port, bus_index):
        client = self._server.client
        # we set both in and out ports to the same bus
        client.send_message('/n_set', [out_port.module.node, out_port.name, bus_index])
        client.send_message('/n_set', [in_port.module.node, in_port.name, bus_index])


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
