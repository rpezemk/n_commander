import curses
import signal
import asyncio
from typing import Any

from tui import signal_resolver
from tui.visual_grid import MainGrid
from nosc.twin_service import TwinService
import ui_layout
from utils.async_processor import AsyncProcessor

async def update_progress_bar():
    while True:
        ui_layout.prog_bar_value = ((ui_layout.prog_bar_value * 10 + 10) % 1000)/10
        await asyncio.sleep(0.05)
        
async def start_update_progress_bar():
        asyncio.create_task(update_progress_bar())


def main(stdscr):
    try:
        signal_resolver.init_screen(stdscr)
        asyncio.run(ui_layout.vg.set_stdscr(stdscr).run_async_tasks(stdscr, [start_update_progress_bar]))
    except:
        ...

def server_message_handler(address, *args):
    # keep line below for testing purpose
    # print(f"Received message at {address}: {args}")
    ...


def wrap():
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    twin_service = TwinService("127.0.0.1", 8002, [("/*", server_message_handler)])
    twin_service.push_message(("/test", [99, "Hello OSC!"]))
    async_proc = AsyncProcessor([twin_service.start_server, twin_service.start_client]).start()
    curses.wrapper(main);
    
if __name__ == "__main__":
    wrap()

