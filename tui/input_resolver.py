import curses
import sys
import os
from pathlib import Path
from datetime import datetime
import asyncio
from typing import Callable, Any

from utils import os_utils, string_utils
from tui import signal_resolver
from tui.visual_grid import VisualGrid
from tui.measures import Area, Segment, Length, LenT
from tui.placements import GPlace
from tui.text_box import TBox
from tui.controls import Btn, Clock, HPanel, DirP, BaseVisual, ListView
from tui.placements import PPlace, HPosEnum
import tui.n_window
from tui.n_window import NWindow, ColInfo


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