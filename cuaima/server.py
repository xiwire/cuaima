from pythonosc import udp_client, osc_server


DEFAULT_SERVER_ADDRESS = '127.0.0.1'
DEFAULT_SERVER_PORT = 57110


class Server:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port

        dispatcher = osc_server.Dispatcher()
        dispatcher.map('/status.reply', print)
        server_address = (self.address, self.port+1)
        self.server = osc_server.ThreadingOSCUDPServer(server_address=server_address,
                                                       dispatcher=dispatcher)
        # self.server.serve_forever()

    def generate_client(self) -> udp_client.SimpleUDPClient:
        """ Returns a client to the server
        """
        return udp_client.SimpleUDPClient(self.address, self.port)


DEFAULT_SERVER = Server(address=DEFAULT_SERVER_ADDRESS, port=DEFAULT_SERVER_PORT)


class TalksToServerMixin:
    """ Mixin for classes that talk to the server
    """
    def __init__(self, server):
        self.server = server
        self._client = None

    @property
    def client(self):
        """ Returns a suitable client to talk to the server
        """
        if self._client is None:
            self._client = self.server.generate_client()
        # TODO: handle reconnections maybe
        return self._client
