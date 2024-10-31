import curses
import os
from pathlib import Path
from datetime import datetime
import asyncio
from dataclasses import dataclass

from tui import signal_resolver
from tui.measures import Area
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
        pass


@dataclass
class TuiStyles():
    double = TuiSet("\u2550",
                    "\u2551",
                    "\u2554",
                    "\u2557",
                    "\u255A",
                    "\u255D")
    
    single = TuiSet("\u2500",
                    "\u2502",
                    "\u250C",
                    "\u2510",
                    "\u2514",
                    "\u2518")

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
        # self.win.border(".", ".", ".", ".", ".", ".", ":", ":")        
        pass
    
    
    def draw_border(self):
        h, w = self.area.get_dims()
        test = [TuiStyles.single.top_left + (w-2) * TuiStyles.single.horizontal + TuiStyles.single.top_right, 
                *( (h-2) * [TuiStyles.single.vertical + (w - 2) * " " + TuiStyles.single.vertical]), 
                TuiStyles.single.bottom_left + (w-2) * TuiStyles.single.horizontal + TuiStyles.single.bottom_right]
        frame.draw_area(area=self.area, sub_lines=test)
        return self
          
    def addstr(self, y0, x0, text: str = ''):
        base_area = self.area
        width = len(text)
        
        res_y0 = y0 + self.area.y0
        res_x0 = x0 + self.area.x0
        res_area = Area(res_y0, res_x0, res_y0, res_x0 + width - 1)
        frame.draw_area(area=res_area, sub_lines=[text])
        ... 
        
    