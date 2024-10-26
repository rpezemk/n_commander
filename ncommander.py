import curses
import os
from utils import os_utils, string_utils
import asyncio
from datetime import datetime
from tui import signal_resolver
from tui.controls import (
    Button, ClockButton, HStackPanel, MainView,
    ItemPanel, HPosEnum, DirPanel, LogPanel,
)

app_is_running = True
clock = ClockButton("", hPos=HPosEnum.RIGHT)
log_panel = LogPanel("[LOGGER]")

mouse_actions = [curses.BUTTON1_CLICKED, curses.BUTTON3_CLICKED,
                    curses.BUTTON1_DOUBLE_CLICKED, curses.BUTTON3_DOUBLE_CLICKED,
                    curses.BUTTON1_PRESSED, curses.BUTTON3_PRESSED]


async def resolve_input_continous(stdscr, log_panel: LogPanel):
    global app_is_running
    while app_is_running:
        key = stdscr.getch()
        if key == -1:
            pass
        elif key == curses.KEY_MOUSE:
            id, mx, my, mz, bs = curses.getmouse()
            log_panel.log(f"M: k:{key}, bs:{bs} ({my}, {mx}, {mz})")
        elif key == ord("q"):
            app_is_running = False
        else:
            log_panel.log(f"K: k:{key}")
        
        await asyncio.sleep(0.01)


menu = HStackPanel(
    [
        Button("edit"), Button("view"), Button("settings"),
        Button("help"), Button("about"), clock,
    ]
)

curr_path = os.path.abspath(".")
quad_items = [
    DirPanel(curr_path), log_panel,
    DirPanel(curr_path), DirPanel(curr_path),
]


async def async_tui_refresh(quad: MainView):
    while app_is_running:
        quad.refresh_quad()
        await asyncio.sleep(0.1)

async def async_slow_refresh():
    while app_is_running:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clock.update_time(now)
        await asyncio.sleep(0.1)
        

async def run_async_tasks(stdscr):
    global app_is_running
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    stdscr.nodelay(True)  # Non-blocking mode
    quad = MainView(stdscr, quad_items, menu)
    slow_task = asyncio.create_task(async_slow_refresh())
    input_task = asyncio.create_task(resolve_input_continous(stdscr, log_panel))
    tui_task = asyncio.create_task(async_tui_refresh(quad))
    await tui_task


def main(stdscr):
    signal_resolver.init_screen(stdscr)
    asyncio.run(run_async_tasks(stdscr))


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"Error: {e}")
