import curses
import os
from pathlib import Path
from datetime import datetime
import asyncio
import locale
from typing import Any
from dataclasses import dataclass


import tui.elementary.measures

from tui.elementary.ts import TS
from tui import signal_resolver
from tui.elementary.measures import Area, Length, Segment, Col, LenT
from tui.frame_buffer.frame import Frame

stdscr = None

frame: Frame = None

def get_frame():
    global frame
    return frame


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
    
    
    def draw_table(self):
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
        

