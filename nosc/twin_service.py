from concurrent.futures import ThreadPoolExecutor
import select
import signal
from typing import Callable, Tuple
from pythonosc import udp_client
import time
import asyncio
from pythonosc import osc_server
from pythonosc import dispatcher

def server_message_handler(address, *args):
    print(f"Received message at {address}: {args}")

class TwinService():
    def __init__(self, ip, port, handlers: list[(str, Callable)]):
        self.ip = ip
        self.port = port
        self.handlers = handlers
        self.client = None
        self.messages = []
    
    def push_message(self, message: Tuple[str, list]):
        self.messages.append(message)
        
    async def start(self):
        asyncio.create_task(self.start_server())    
        asyncio.create_task(self.start_client())
        
    async def start_client(self):
        client = udp_client.SimpleUDPClient(self.ip, self.port)
        while True:
            if any(self.messages):
                m = self.messages[-1]
                client.send_message(m[0], m[1])
                print("message sent!")
            await asyncio.sleep(1)
        
    async def start_server(self):
        disp = dispatcher.Dispatcher()
        for handler in self.handlers:
            disp.map(*handler)  
        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), disp)
        self.server.timeout = 0.005
        sock = self.server.socket
        print(f"Serving on {self.server.server_address}")
        while True:
            ready_to_read, _, _ = select.select([sock], [], [], 0.1)  
            if ready_to_read:    
                self.server.handle_request()  
            await asyncio.sleep(0.005)  

    

async def run_async_tasks():
    try:
        server_task = asyncio.create_task(my_service.start_server())
        asyncio.create_task(my_service.start_client())
        await server_task
    except:
        ...

if __name__ == "__main__":
    my_service = TwinService("127.0.0.1", 8001, [("/*", server_message_handler)])
    my_service.push_message(("/test", [99, "Hello OSC!"]))
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    asyncio.run(run_async_tasks())
