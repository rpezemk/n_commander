import curses
import os
from utils import os_utils, string_utils
import asyncio
from asyncio import TaskGroup
from datetime import datetime
from tui import signal_resolver
from tui.controls import FillMethod, Button, HStackPanel, MyWindow, QuadView, ItemPanel

now = "<init now>"

class ClockButton(Button):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)

    def draw(self, x0):
        self.title = now # datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

quad_items = [
    ItemPanel(curr_path, fill_window),
    ItemPanel(kojaja, fill_window),
    ItemPanel(curr_path, fill_window),
    ItemPanel(curr_path, fill_window)
]   

menu = HStackPanel([
            Button("edit"),
            Button("view"),
            Button("settings"),
            Button("help"),
            Button("about"),
            ClockButton("")
            ])     

def main(stdscr):
    signal_resolver.init_screen(stdscr)
    quad = QuadView(stdscr, quad_items, menu)
    while True:    
        quad.refresh_quad()
        key = stdscr.getch()
        if key == ord('q'):
            break
        
async def background_task():
    global now
    while True:
        await asyncio.sleep(1)  # Non-blocking sleep
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Background task updated: {now}")

# Async function to wrap the curses application
async def async_main():
    curses.wrapper(main)

# Async function to run both the curses app and background task concurrently
async def group_main():
    # Create the background task outside the TaskGroup so it runs independently
    background = asyncio.create_task(background_task())

    # Now, run the curses interface
    async with asyncio.TaskGroup() as group:
        group.create_task(async_main())
    

    background.cancel()
    await background

# Run the async wrapper
if __name__ == "__main__":
    # Start the group of tasks
    asyncio.run(group_main())