import curses
import signal
import asyncio
from typing import Any

from tui import signal_resolver
from utils.twin_service import TwinService
import ui_layout
from utils.async_processor import AsyncProcessor
import msg_handlers
        
def main(stdscr):
    try:
        signal_resolver.init_screen(stdscr)
        asyncio.run(ui_layout.vg.set_stdscr(stdscr).run_async_tasks())
    except:
        ...
        
def wrap():
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    twin_service = TwinService("127.0.0.1", 8002, msg_handlers.msg_handlers)
    twin_service.push_message(("/test", [99, "Hello OSC!"]))
    async_proc = AsyncProcessor(
        [
            twin_service.start_server, 
            twin_service.start_client, 
            *ui_layout.non_ui_tasks
        ])
    async_proc.start()
    curses.wrapper(main);
    
if __name__ == "__main__":
    wrap()

