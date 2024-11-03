import asyncio
import curses
from enum import Enum
from typing import Callable
from tui.elementary.measures import LenT, Length
from tui.controls import BaseVisual, HPosEnum
from tui.elementary.placements import GPlace, PPlace
from tui.elementary.measures import Area, Segment
import tui.elementary.measures
import tui.signal_resolver
from tui.input_resolver import InputResolver


def soft_close_app():
    ...
    
def log_to_panel(key, id, mx, my, mz, bs): 
    ...
    


class MainGrid(BaseVisual):
    def __init__(self, children: list[BaseVisual] = None, 
                 area: Area = Area(), 
                 g_place: GPlace = GPlace(0, 0, 0, 0), 
                 panel_placement: PPlace = PPlace(),
                 row_defs: list[Length] = [Length(100, LenT.STAR)],
                 col_defs: list[Length] = [Length(100, LenT.STAR)],
                 stdscr = None
                 ):
        # row_defs = [(1, "a"), (50, "*"), (50, "*")]
        res_row_defs = []
        
        super().__init__(None, children, area, g_place, panel_placement)
        self.row_defs = row_defs
        self.col_defs = col_defs
        self.stdscr = stdscr
        self.app_is_running = True
        
        self.input_resolver = InputResolver(None, 
                               get_scr_func=(lambda: tui.signal_resolver.stdscr), 
                               root_obj_func=lambda: self, 
                               turn_off_func=lambda: self.close_app(),
                               report_click_func=log_to_panel)
        
    def draw(self):
        self.area = Area(0, 0, *self.stdscr.getmaxyx())
        h, w = self.get_dims()
        v_lengths = tui.elementary.measures.get_segments(self.row_defs, h - 1)
        h_lengths = tui.elementary.measures.get_segments(self.col_defs, w - 1)
        
        for ch in self.children:
            if ch == None:
                continue
            
            row_no = ch.g_place.row_no
            row_sp = ch.g_place.row_span
            col_no = ch.g_place.col_no
            col_sp = ch.g_place.col_span
            
            v_sub = v_lengths[row_no:row_no+row_sp]
            h_sub = h_lengths[col_no:col_no+col_sp]
            
            v_seg = v_sub[0]
            h_seg = h_sub[0]
            v_sum = sum([h.diff() for h in v_sub]) - 1
            h_sum = sum([h.diff() for h in h_sub]) - 1
            ch.area = Area(v_seg.v0, h_seg.v0, v_seg.v0+v_sum, h_seg.v0+h_sum)
            ch.draw()
    
    def close_app(self):
        self.app_is_running = False
    
    async def run_async_tasks(self, stdscr, tasks: list[Callable[[],None]] = []):
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        stdscr.nodelay(True)  # Non-blocking mode

        for t in tasks:
            asyncio.create_task(t())
        input_task = asyncio.create_task(self.input_resolver.start())
        tui_task = asyncio.create_task(self.async_grid_refresh())
        await tui_task
        stdscr.clear()
        stdscr.refresh()
        
    async def async_grid_refresh(self):
        while self.app_is_running:
            self.draw()
            tui.n_window.render_frame()
            await asyncio.sleep(0.1)