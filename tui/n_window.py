import curses
import os
from pathlib import Path
from datetime import datetime
import asyncio

from tui import signal_resolver
from tui.measures import Area

stdscr = None

class Frame():
    """it's not what you think it is
    """
    def __init__(self, stdscr):
        max_y, max_x = signal_resolver.stdscr.getmaxyx()
        self.lines:list[str] = max_x * [max_y * " "]
        self.stdscr = stdscr
        pass
    
    def draw(self):
        ...
    def draw_window(self, n_window: 'NWindow'=None):
        max_y, max_x = signal_resolver.stdscr.getmaxyx()
        area = n_window.area
        height, width = area.get_dims()
        # Draw top and bottom borders
        self.draw_h_line(area.y0, area.x0, width - 2, "*")
        self.draw_h_line(area.y0 + height - 1, area.x0, width - 2, "*")
    
        # Draw left and right borders
        
        self.draw_v_line(area.y0, area.x0, height - 1, "*")
        self.draw_v_line(area.y0, area.x0 + width - 1, height - 1, "*")
            

        # Refresh the screen to show the changes
        signal_resolver.stdscr.refresh()

        ...
        
    def draw_h_line(self, y0, x0, len, ch: str):
        signal_resolver.stdscr.addstr(y0, x0, ch*len)
        line = self.lines[y0]
        res = line[:x0] + ch*len
        signal_resolver.stdscr.addstr(y0, 0, res)
        
    def draw_v_line(self, y0, x0, len, ch: str):
        for i in range(0, len):
            signal_resolver.stdscr.addstr(y0 + i, x0, ch)
        
class NWindow(): #h + 1, w + 1, self.area.y0, self.area.x0
    def __init__(self, h: int, w: int, y0: int, x0: int, title = ""): 
        self.area = Area(y0, x0, y0 + h - 1, x0 + w - 1)
        self.win = curses.newwin(h, w, y0, x0)
        self.title = title    
        self.border_data = (" ", " ", " ", " ", " ", " ", " ", " ",)
        # self.win.border(".", ".", ".", ".", ".", ".", ":", ":")        
        pass
    
    
    def with_border(self):
        self.win.border(".", ".", ".", ".", ".", ".", ":", ":")
        self.win.addstr(0, 2, self.title)
        # Frame(signal_resolver.stdscr).draw_window(self)
        return self
          
    def addstr(self, y0, x0, text: str = ''):
        self.win.addstr(y0, x0, text)
        
    def refresh(self):
        self.win.refresh()
        ...