import curses
import os
from utils import os_utils, string_utils
import asyncio
from asyncio import TaskGroup
from datetime import datetime
from tui import signal_resolver
from tui.controls import FillMethod, Button, HStackPanel, MyWindow, QuadView, ItemPanel

now = None

class ClockButton(Button):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)

    def draw(self, x0):
        self.title = now 
        self.real_title = f"[{self.title}]"
        super().draw(x0)
        
def fill_window(myWindow: MyWindow) -> None:
    height = myWindow.y1 - myWindow.y0
    width = myWindow.x1 - myWindow.x0
    win = curses.newwin(height, width, myWindow.y0, myWindow.x0)  
    win.border()
    win.addstr(0, 1, myWindow.title)
    dirOk, dirs, files, errStr = os_utils.try_get_dir_content(myWindow.title)
    if dirOk:
        content = string_utils.list_to_columns(height - 3, width - 1, dirs + files)
        myWindow.title = os.path.abspath(myWindow.title)
        for idx, line in enumerate(content):
            if idx > myWindow.y1 - myWindow.y0 - 3:
                break
            win.addstr(1 + idx, 3, line)  
    else:
        pass
    win.refresh()
    
kojaja = "/home/kojaja/"
curr_path = os.path.abspath('.')


menu = HStackPanel([
            Button("edit"),
            Button("view"),
            Button("settings"),
            Button("help"),
            Button("about"),
            ClockButton("")
            ])     

quad_items = [
    ItemPanel(curr_path, fill_window),
    ItemPanel(kojaja, fill_window),
    ItemPanel(curr_path, fill_window),
    ItemPanel(curr_path, fill_window)
]   
        
async def async_main(stdscr):
    signal_resolver.init_screen(stdscr)
    quad = QuadView(stdscr, quad_items, menu)
    while True:
        quad.refresh_quad()
        key = stdscr.getch()
        if key == ord('q'):
            break
        await asyncio.sleep(0.1)

app_is_running = False

async def background_task():
    global now
    while app_is_running:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await asyncio.sleep(0.1)  
        
async def run_curses_and_tasks():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    global app_is_running
    app_is_running = True
    try:
        background = asyncio.create_task(background_task())
        await async_main(stdscr)
        app_is_running = False
        await background
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        background.cancel()
        await background  

if __name__ == "__main__":
    try:
        asyncio.run(run_curses_and_tasks())
    except Exception as e:
        print(f"Error: {e}")
