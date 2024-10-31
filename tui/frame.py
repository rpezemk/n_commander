import curses
import os
from pathlib import Path
from datetime import datetime
import asyncio

from tui import signal_resolver
from tui.measures import Area


class Frame():
    """it's not what you think it is
    """
    def __init__(self, stdscr):
        self.n_rows, self.n_cols = signal_resolver.stdscr.getmaxyx()        
        self.lines:list[str] = (self.n_rows)  * [(self.n_cols) * " "]      
        self.prev_lines:list[str] = (self.n_rows)  * [(self.n_cols) * " "]   
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
            pass
    
    def render_line(self, y0, line: str):
        pad = curses.newpad(1, self.n_cols)
        pad.insstr(0, 0, line)
        pad.refresh(0, 0, y0, 0, y0, self.n_cols-1)
        pass 
    
    def render(self):
        if signal_resolver.stdscr is None:
            return
        
        needs_refresh = False
                
        try:
            n_rows, n_cols = signal_resolver.stdscr.getmaxyx()        
            for idx in range(0, n_rows - 1):
                prev_line = self.prev_lines[idx]
                curr_line = self.lines[idx]
                curr_len = len(curr_line)
                
                if curr_line != prev_line:
                    needs_refresh = True
                    self.render_line(idx, curr_line)
                    self.prev_lines[idx] = self.lines[idx]
                    
            idx = n_rows - 1
            prev_line = self.prev_lines[idx]
            curr_line = self.lines[idx]
            if curr_line != prev_line:
                needs_refresh = True
                self.render_line(idx, curr_line)
                self.prev_lines[idx] = self.lines[idx]
  
        except Exception as e:
            pass

                  

