import curses
import os
from pathlib import Path
from datetime import datetime
import asyncio
from typing import Tuple
from tui import signal_resolver
from tui.measures import Area


class Frame():
    """it's not what you think it is
    """
    def __init__(self, stdscr):
        self.n_rows, self.n_cols = signal_resolver.stdscr.getmaxyx()        
        self.lines:list[str] = (self.n_rows)  * [(self.n_cols) * " "]      
        self.prev_lines:list[str] = (self.n_rows)  * [(self.n_cols) * " "]   
        self.lines_to_refresh: list[Tuple[int, str]] = []
        self.pad = curses.newpad(self.n_rows, self.n_cols)
        pass
    
    def draw_area(self, area:Area = Area(), sub_lines: list[str] = []):
        height, width = area.get_dims()
        for idx in range(0, min(height, len(sub_lines))):
            if area.y0 + idx >= len(self.lines):
                break
            dest_line = self.lines[area.y0 + idx]
            sub_line = sub_lines[idx]
            begin = dest_line[:area.x0]
            end = dest_line[area.x0 + len(sub_line):]
            self.lines[area.y0 + idx] = begin + sub_line + end
    
    def set_line(self, y0, line: str):
        self.pad.insstr(y0, 0, line)
        self.pad.refresh(0, 0, 0, 0, y0, self.n_cols-1)
    
    def refresh_pad(self):
        self.pad.refresh(0, 0, 0, 0, self.n_rows - 1, self.n_cols-1)
        
    
    def render_frame(self):
        if signal_resolver.stdscr is None:
            return
        self.lines_to_refresh = []
        try:
            n_rows, n_cols = signal_resolver.stdscr.getmaxyx()        
            for idx in range(0, n_rows):                
                if self.lines[idx] != self.prev_lines[idx]:
                    self.lines_to_refresh.append((idx, self.lines[idx]))
                    self.prev_lines[idx] = self.lines[idx]
                           
            for idx, line in self.lines_to_refresh:
                self.set_line(idx, line)
            
            if len(self.lines_to_refresh) > 0:
                self.refresh_pad()    
            
        except Exception as e:
            pass

                  

