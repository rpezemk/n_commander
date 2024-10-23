import curses
from curses import endwin
from enum import Enum
import signal
from pathlib import Path
import os
import time
from typing import Callable

from utils import enum_utils
from utils import os_utils
from utils import string_utils

from tui import signal_resolver
from tui.controls import VisualHierarchy, FillMethod, Button, HStackPanel, MyWindow, QuadView
from tui.splash import splashContent




stdscr = None
helloWashShown = False;
    

def resize_handler(signum, frame):
    signal_resolver.handle(stdscr)


def fill_window(myWindow: MyWindow) -> None:
    win = curses.newwin(myWindow.y1 - myWindow.y0,myWindow.x1 - myWindow.x0, myWindow.y0, myWindow.x0)  
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
    
    
def main(stdscr_local):
    signal.signal(signal.SIGWINCH, resize_handler) 
    global stdscr
    stdscr = stdscr_local
    stdscr_local.clear()
    # curses.mousemask(curses.ALL_MOUSE_EVENTS)
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        
    global helloWashShown
    
    if not helloWashShown:
        lines = splashContent.splitlines()
        
        for idx, line in enumerate(lines):
            stdscr.addstr(idx, 2, line)  
            
        stdscr.refresh()  
        stdscr.getch() 
        pass
    
    helloWashShown = True;
    signal_resolver.redraw_stdscreen(stdscr)
    
    while True:
        menu = HStackPanel([
            Button("edit"),
            Button("view"),
            Button("settings"),
            Button("help"),
            Button("about")])
        
        y0 = 1
        yMax, xMax = stdscr.getmaxyx()
        x1 = int(xMax/2)
        x2 = xMax 
        y1 = int(yMax/2)
        y2 = yMax
        
        currPath = os_utils.make_abs_path()
        
        quadItems = [
            MyWindow(currPath, None, [], y0, 0, y1, x1),
            MyWindow("/home/kojaja/", None, [], y0, x1, y1, x2),
            MyWindow(currPath, None, [], y1, 0, y2, x1),
            MyWindow(currPath, None, [], y1, x1, y2, x2)
        ]
        
        tiled = QuadView(
            stdscr_local, None, quadItems, 
            0, 0, 0, 0, 
            FillMethod.ITEM_PANEL_ROWS_COLS, 
            menu, 
            fill_window)

        tiled.StartQuad()
        key = stdscr.getch()
        if key == ord('q'):
            break


    
curses.wrapper(main)
