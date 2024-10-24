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
from tui.controls import VisualHierarchy, FillMethod, Button, HStackPanel, MyWindow, QuadView
from tui.splash import splash_content

hello_was_shown = False;
    

def fill_window(myWindow: MyWindow) -> None:
    win = curses.newwin(myWindow.y1 - myWindow.y0, myWindow.x1 - myWindow.x0, myWindow.y0, myWindow.x0)  
    win.border()
    win.addstr(0, 1, myWindow.title)
    inputContent, corrPath = os_utils.list_directory_content(myWindow.title)
    content = string_utils.list_to_columns(myWindow.y1 - myWindow.y0 - 3, myWindow.x1 - myWindow.x0 - 1, inputContent)
    myWindow.title = corrPath
    for idx, line in enumerate(content):
        if idx > myWindow.y1 - myWindow.y0 - 3:
            break
        win.addstr(1 + idx, 3, line)  
    win.refresh()
    
    
def main(stdscr):
    signal_resolver.init_screen(stdscr)
    global hello_was_shown
    
    if not hello_was_shown:
        lines = splash_content.splitlines()
        
        for idx, line in enumerate(lines):
            signal_resolver.stdscr.addstr(idx, 2, line)  
            
        signal_resolver.stdscr.refresh()  
        signal_resolver.stdscr.getch() 
        pass
    
    hello_was_shown = True;
    
    while True:
        menu = HStackPanel([
            Button("edit"),
            Button("view"),
            Button("settings"),
            Button("help"),
            Button("about")])
        
        y0 = 1
        yMax, xMax = signal_resolver.stdscr.getmaxyx()
        x1 = int(xMax/2)
        x2 = xMax 
        y1 = int(yMax/2)
        y2 = yMax
        
        curr_path = os_utils.make_abs_path()
        
        quad_items = [
            MyWindow(curr_path, None, [], y0, 0, y1, x1, None, fill_window),
            MyWindow("/home/kojaja/", None, [], y0, x1, y1, x2, None, fill_window),
            MyWindow(curr_path, None, [], y1, 0, y2, x1, None, fill_window),
            MyWindow(curr_path, None, [], y1, x1, y2, x2, None, fill_window)
        ]
        
        tiled = QuadView(
            stdscr, None, quad_items, 
            0, 0, 0, 0, 
            FillMethod.ITEM_PANEL_ROWS_COLS, 
            menu)

        tiled.start_quad()
        key = signal_resolver.stdscr.getch()
        if key == ord('q'):
            break


    
curses.wrapper(main)
