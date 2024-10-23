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
from tui.controls import VisualHierarchy, FillMethod
from tui.splash import splashContent




stdscr = None
helloWashShown = False;
    

def resize_handler(signum, frame):
    signal_resolver.handle(stdscr)




class Button(VisualHierarchy):
    def __init__(self, title: str, parent = None):
        super().__init__(parent)
        self.title = title
        self.realTitle = f"[{self.title}]"
        
    def draw(self, x0):
        win = curses.newwin(3 , len(self.realTitle), 0, x0)  
        win.addstr(0, 0, self.realTitle)
        win.refresh()

    def getWidth(self):
        return len(self.realTitle)
    

    
class HStackPanel(VisualHierarchy):
    def __init__(self, list, parent = None, children = []):
        super().__init__(parent, children)
        self.items = list
        
    def addItem(self, item):
        self.items.append(item)

    def draw(self):
        currX = 1
        for item in self.items:
            item.draw(currX)
            currX += item.getWidth() + 1
            
class MyWindow(VisualHierarchy):
    def __init__(self, title: str, parent = None, children = [], y0 = 0, x0 = 0, y1 = 0, x1 = 0, fillMethod: FillMethod = FillMethod.ITEM_PANEL_ROWS_COLS):
        super().__init__(parent, children, y0, x0, y1, x1, fillMethod)
        self.title = title
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        # self.contentFunc = contentFunc
    
    def getContent(self) -> str:
        pass
    
    def interact(self, ch: int):
        pass
    
    def draw(self):
        win = curses.newwin(self.y1 - self.y0,self.x1 - self.x0, self.y0, self.x0)  
        win.border()
        win.addstr(0, 1, self.title)
        win.refresh()
       
class DirWindow(MyWindow):
    def __init__(self, path: str, parent = None, children = [], 
                 y0 = 0, x0 = 0, y1 = 0, x1 = 0, 
                 fillMethod: FillMethod = FillMethod.ITEM_PANEL_ROWS_COLS):
        super().__init__(path, parent, children, y0, x0, y1, x1, fillMethod)
        self.content, corrPath = os_utils.list_directory_content(path)
        self.title = str(corrPath)
        
    def draw(self):
        win = curses.newwin(self.y1 - self.y0,self.x1 - self.x0, self.y0, self.x0)  
        win.border()
        win.addstr(0, 1, self.title)
        content = string_utils.list_to_columns(self.y1 - self.y0 - 3, self.x1 - self.x0 - 1, self.content)
        for idx, line in enumerate(content):
            if idx > self.y1 - self.y0 - 3:
                break
            win.addstr(1 + idx, 3, line)  
        win.refresh()

    
class MainView(VisualHierarchy):
    def __init__(self, stdscr, parent = None, children = [], 
                 y0 = 0, x0 = 0, y1: int = 0, x1: int = 0, 
                 fillMethod: FillMethod = FillMethod.ITEM_PANEL_ROWS_COLS):
        super().__init__(parent, children, y0, x0, y1, x1, fillMethod)
        self.stdscr = stdscr
    
    def StartQuad(self):
        yMax, xMax = self.stdscr.getmaxyx()
        x1 = int(xMax/2)
        x2 = xMax 
        y1 = int(yMax/2)
        y2 = yMax
                
        self.menuPanel = HStackPanel([
            Button("edit"),
            Button("view"),
            Button("settings"),
            Button("help"),
            Button("about")])
         
        self.menuPanel.draw()
        y0 = 4
        self.appendChild(DirWindow(".", self, [], y0, 0, y1, x1))
        self.appendChild(DirWindow("/home/kojaja/", self, [], y0, x1, y1, x2))
        self.appendChild(DirWindow(".", self, [], y1, 0, y2, x1))
        self.appendChild(DirWindow(".", self, [], y1, x1, y2, x2))
        
        self.menuPanel.draw()
        for myWin in self.children:
            myWin.draw()
        self.stdscr.refresh()
        
    

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
        tiled = MainView(stdscr_local)
        tiled.StartQuad()
        key = stdscr.getch()
        if key == ord('q'):
            break

     
curses.wrapper(main)
