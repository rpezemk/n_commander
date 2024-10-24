import curses
from curses import endwin
from enum import Enum
import signal
from pathlib import Path
import os
import time
from typing import Callable

from utils import enum_utils, os_utils, string_utils

from tui import signal_resolver
from tui.controls import VisualHierarchy, FillMethod, Button, HStackPanel, MyWindow, QuadView, ItemPanel


    

def fill_window(myWindow: MyWindow) -> None:
    height = myWindow.y1 - myWindow.y0
    width = myWindow.x1 - myWindow.x0
    win = curses.newwin(height, width, myWindow.y0, myWindow.x0)  
    win.border()
    win.addstr(0, 1, myWindow.title)
    dirOk, dirs, files, errStr = os_utils.try_get_dir_content(myWindow.title)
    if dirOk:
        content = string_utils.list_to_columns(height - 3, width - 1, dirs + files)
        myWindow.title = os.path.abspath(myWindow.title)
        for idx, line in enumerate(content):
            if idx > myWindow.y1 - myWindow.y0 - 3:
                break
            win.addstr(1 + idx, 3, line)  
    else:
        pass
    win.refresh()
    
    
def main(stdscr):
    signal_resolver.init_screen(stdscr)
    
    while True:
        menu = HStackPanel([
            Button("edit"),
            Button("view"),
            Button("settings"),
            Button("help"),
            Button("about")])
        
        kojaja = "/home/kojaja/"
        curr_path = os.path.abspath('.')

        quad_items = [
            ItemPanel(curr_path, fill_window),
            ItemPanel(kojaja, fill_window),
            ItemPanel(curr_path, fill_window),
            ItemPanel(curr_path, fill_window)
        ]
        
        yMax, xMax = signal_resolver.stdscr.getmaxyx()
        tiled = QuadView(
            stdscr, None, quad_items, 
            0, 0, yMax, xMax, 
            FillMethod.ITEM_PANEL_ROWS_COLS, 
            menu)

        tiled.start_quad()
        key = signal_resolver.stdscr.getch()
        if key == ord('q'):
            break

curses.wrapper(main)
