import time
from typing import Callable, NoReturn, Tuple
import signal
import threading
import select

from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import dispatcher
from pythonosc.osc_server import OSCUDPServer

class TwinService():
    def __init__(self, ip, port, handlers: list[(str, Callable)]):
        self.ip = ip
        self.port = port
        self.handlers = handlers
        self.client = None
        self.messages = []
        self.server: OSCUDPServer = None
        
    def push_message(self, message: Tuple[str, list]):
        self.messages.append(message)
        
    def start_client(self) -> NoReturn:
        client = udp_client.SimpleUDPClient(self.ip, self.port)
        while True:
            if any(self.messages):
                m = self.messages[-1]
                client.send_message(m[0], m[1])
            time.sleep(1)
        
    def start_server(self) -> NoReturn:
        disp = dispatcher.Dispatcher()
        for handler in self.handlers:
            disp.map(*handler)  
        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), disp)
        self.server.timeout = 0.01
        sock = self.server.socket
        while True:
            ready_to_read, _, _ = select.select([sock], [], [], 0.1)  
            if ready_to_read:    
                self.server.handle_request()  
            time.sleep(0.11)  

    def gently_close(self):
        self.server.server_close()
