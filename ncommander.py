import curses
import os
from utils import os_utils, string_utils
import asyncio
from datetime import datetime
from tui import signal_resolver
from tui.controls import (
    Button,
    ClockButton,
    HStackPanel,
    MyWindow,
    MainView,
    ItemPanel,
    HPosEnum,
)

now = None
app_is_running = False
clock = ClockButton("", hPos=HPosEnum.RIGHT)


def update_slow():
    global now
    global clock
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clock.update_time(now)


def update_fast():
    pass


def resolve_input():
    global app_is_running
    key = signal_resolver.stdscr.getch()
    if key == ord("q"):
        app_is_running = False


async def assign_recurrent(period_ms: int, func):
    while app_is_running:
        func()
        await asyncio.sleep(period_ms / 1000)


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


def is_mouse_click(click) -> bool:
    return click == curses.KEY_MOUSE


kojaja = "/home/kojaja/"
curr_path = os.path.abspath(".")


menu = HStackPanel(
    [
        Button("edit"),
        Button("view"),
        Button("settings"),
        Button("help"),
        Button("about"),
        clock,
    ]
)

quad_items = [
    ItemPanel(curr_path, fill_window),
    ItemPanel(kojaja, fill_window),
    ItemPanel(curr_path, fill_window),
    ItemPanel(curr_path, fill_window),
]


async def async_main(stdscr):
    global app_is_running
    signal_resolver.init_screen(stdscr)
    quad = MainView(stdscr, quad_items, menu)
    while app_is_running:
        quad.refresh_quad()
        await asyncio.sleep(0.1)


async def run_curses_and_tasks():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    global app_is_running
    app_is_running = True
    try:
        background = asyncio.create_task(assign_recurrent(100, update_slow))
        background = asyncio.create_task(assign_recurrent(10, update_fast))
        background = asyncio.create_task(assign_recurrent(1, resolve_input))
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
