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
        self.client = udp_client.SimpleUDPClient(self.address, self.port)


DEFAULT_SERVER = Server(address=DEFAULT_SERVER_ADDRESS, port=DEFAULT_SERVER_PORT)
