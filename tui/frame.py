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
        max_y, max_x = signal_resolver.stdscr.getmaxyx()
        self.lines:list[str] = (max_y)  * [(max_x) * " "]      
        pass
    
    def draw_area(self, area:Area = Area(), sub_lines: list[str] = []):
        
        height, width = area.get_dims()
        for idx in range(0, min(height, len(sub_lines))):
            if area.y0 + idx >= len(self.lines):
                break
            in_len = len(self.lines[area.y0 + idx])
            dest_line = self.lines[area.y0 + idx]
            sub_line = sub_lines[idx]
            begin = dest_line[:area.x0]
            end = dest_line[area.x0 + len(sub_line):]
            res = begin + sub_line + end
            self.lines[area.y0 + idx] = res
            out_len = len(self.lines[area.y0 + idx])
            diff = out_len - in_len
            pass
    
    def render(self):
        if signal_resolver.stdscr is None:
            return
        
        max_y, max_x = signal_resolver.stdscr.getmaxyx()
        
        try:
            pass
            n_rows, n_cols = signal_resolver.stdscr.getmaxyx()        
            lengths = [len(l) for l in self.lines]
            
            for idx in range(0, n_rows - 1):
                l = self.lines[idx]
                signal_resolver.stdscr.addstr(idx, 0, l[:len(l) - 0])
                
            idx = n_rows - 1
            l = self.lines[idx]
            signal_resolver.stdscr.addstr(idx, 0, l[:len(l) - 1])
            signal_resolver.stdscr.insch(idx, n_cols - 1, l[len(l) - 1])
            signal_resolver.stdscr.refresh()
    
        except Exception as e:
            pass

                  

