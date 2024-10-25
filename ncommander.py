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
    DirPanel,
    LogPanel,
)

now = None
app_is_running = False
clock = ClockButton("", hPos=HPosEnum.RIGHT)
log_panel = LogPanel("[LOGGER]")
log_panel.logLines = [
    "def",
    "def",
    "def",
    "def",
    "def",
    "def",
    "def",
    "def",
    "def",
    "abc",
    "def",
    "some incredibly long line with many characters, so keep it.... :D KOJAJA, maybe try to read Norwid instead, or latin dictionary",
]


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
    if key == -1:
        return
    if key == curses.KEY_MOUSE:
        _, x, y, _, button_state = curses.getmouse()

        if button_state & curses.REPORT_MOUSE_POSITION:
            log_panel.log(f"MOUSE: got {key} key")

    else:
        log_panel.log(f"KBD: got {key} key")
    if key == ord("q"):
        app_is_running = False


async def assign_recurrent(period_ms: int, func):
    while app_is_running:
        func()
        await asyncio.sleep(period_ms / 1000)


def is_mouse_click(click) -> bool:
    return click == curses.KEY_MOUSE


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
    DirPanel(curr_path),
    log_panel,
    DirPanel(curr_path),
    DirPanel(curr_path),
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
