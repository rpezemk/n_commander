import curses
import os
from pathlib import Path
from datetime import datetime
import asyncio
import tui.measures
from tui.measures import LenT, Length
from dataclasses import dataclass

from tui import signal_resolver
from tui.measures import Area, Length, Segment
from tui.frame import Frame
import locale

stdscr = None

frame: Frame = None

class TuiSet():
    def __init__(self, *args: list[str]):
        self.horizontal =   args[0]
        self.vertical =     args[1]
        self.top_left =     args[2]
        self.top_right =    args[3]
        self.bottom_left =  args[4]
        self.bottom_right = args[5]
        self.upper_conn = args[6]
        self.lower_conn = args[7]
        pass


@dataclass
class TS():
    d = TuiSet("\u2550",
                    "\u2551",
                    "\u2554",
                    "\u2557",
                    "\u255A",
                    "\u255D",
                    "\u2566",
                    "\u2569")
    
    s = TuiSet(
                    "\u2500",
                    "\u2502",
                    "\u250C",
                    "\u2510",
                    "\u2514",
                    "\u2518",
                    "\u252c",
                    "\u2534")

def init_frame(stdscr):
    global frame
    frame = Frame(stdscr)

def render_frame():
    if frame is not None:
        frame.render_frame()
        
class NWindow(): #h + 1, w + 1, self.area.y0, self.area.x0
    def __init__(self, h: int, w: int, y0: int, x0: int, title = ""): 
        self.area = Area(y0, x0, y0 + h - 1, x0 + w - 1)
        self.title = title    
        pass
    
    
    def draw_border(self):
        h, w = self.area.get_dims()
        lines = [TS.s.top_left + (w-2) * TS.s.horizontal + TS.s.top_right, 
                *( (h-2) * [TS.s.vertical + (w - 2) * " " + TS.s.vertical]), 
                TS.s.bottom_left + (w-2) * TS.s.horizontal + TS.s.bottom_right]
        frame.draw_area(area=self.area, sub_lines=lines)
        return self
          
    def addstr(self, y0, x0, text: str = ''):
        base_area = self.area
        width = len(text)
        
        res_y0 = y0 + self.area.y0
        res_x0 = x0 + self.area.x0
        res_area = Area(res_y0, res_x0, res_y0, res_x0 + width - 1)
        frame.draw_area(area=res_area, sub_lines=[text])
        ... 
        
        
class ColInfo():
    def __init__(self, title="", width=Length(10, LenT.STAR)):
        self.title = title
        self.width = tui.measures.get_length(width)
        pass
        
class TableWindow(NWindow):
    def __init__(self, h, w, y0, x0, title="", columns:list[ColInfo]=[]):
        super().__init__(h, w, y0, x0, title)    
        self.columns = columns
        self.rows = []
        self.segments = []
    def emit_row(self):
        row = [*len(self.columns) * []]
        
        
    def draw_border(self):
        h, w = self.area.get_dims()
        n_cols = len(self.columns)
        
        blank_width = w - (n_cols - 1) - 2
        filled_width = w - blank_width
        col_widths = list([col.width for col in self.columns])
        segments = tui.measures.get_segments(col_widths, blank_width)
        self.segments = segments
        self.spacers = [Segment(seg.v0+idx, seg.v1+idx) for idx, seg in enumerate(segments)]
        
        test_blank_sum = sum([w.v1 - w.v0 for w in segments])
        
        
        
        top_line = TS.s.top_left + TS.s.upper_conn.join([TS.s.horizontal * (seg.v1 - seg.v0) for seg in segments]) + TS.s.top_right
        mid_line = TS.s.vertical + TS.s.vertical.join([" " * (seg.v1 - seg.v0) for seg in segments]) + TS.s.vertical
        btm_line = TS.s.bottom_left + TS.s.lower_conn.join([TS.s.horizontal * (seg.v1 - seg.v0) for seg in segments]) + TS.s.bottom_right
        
        top_len = len(top_line)
        lines = [top_line, 
                *( (h-2) * [mid_line]), 
                btm_line]
        frame.draw_area(area=self.area, sub_lines=lines)
        return self
        
    def draw_row(self, row_no=0, row_data:list[str] = []):
        n_filled_cols = min(len(self.columns), len(row_data))
        x0 = self.area.x0 + 1
        y0 = self.area.y0 + 1
        h, w = self.area.get_dims()
        if row_no > h - 3:
            return 
        for i in range(0, n_filled_cols):
            seg = self.spacers[i]
            x_offset = x0 + seg.v0
            y_offset = y0 + row_no
            data = row_data[i]
            frame.draw_area(area=Area(y_offset, x_offset, y_offset, x_offset + len(data)), sub_lines=[data])
        