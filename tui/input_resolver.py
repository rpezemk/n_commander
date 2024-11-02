import curses
import asyncio
from typing import Callable
from tui.placements import GPlace
from tui.text_box import TBox
from tui.controls import BaseVisual
import tui.n_window


class InputResolver():
    def __init__(self, stdscr=None, 
                 get_scr_func:Callable=None, 
                 root_obj_func: Callable[[],BaseVisual]=None, turn_off_func:Callable[[],None] = None,
                 report_click_func:Callable[[int, int, int, int, int],None] = None):
        self.stdscr = stdscr
        self.get_scr_func = get_scr_func
        self.is_running = True
        self.visual_objects = root_obj_func
        self.turn_off_func = turn_off_func
        self.report_click_func = report_click_func
        pass

    async def start(self):
        asyncio.create_task(self.continous_job())
                
    async def continous_job(self):
        while self.is_running:
            if self.stdscr is None:
                self.stdscr = None if self.get_scr_func is None else self.get_scr_func()
            if self.stdscr is not None:
                key = self.stdscr.getch()
                if key == -1:
                    pass
                elif key == curses.KEY_MOUSE:
                    id, mx, my, mz, bs = curses.getmouse()
                    if self.report_click_func is not None:
                        self.report_click_func(key, id, mx, my, mz, bs)
                elif key == ord("q") and self.turn_off_func is not None:
                    self.turn_off_func()
            await asyncio.sleep(0.01)