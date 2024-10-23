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

stdscr = None
helloWashShown = False;

hello = """

::::    :::  ::::::::   ::::::::  ::::    ::::  ::::    ::::      :::     ::::    ::: :::::::::  :::::::::: ::::::::: 
:+:+:   :+: :+:    :+: :+:    :+: +:+:+: :+:+:+ +:+:+: :+:+:+   :+: :+:   :+:+:   :+: :+:    :+: :+:        :+:    :+:
:+:+:+  +:+ +:+        +:+    +:+ +:+ +:+:+ +:+ +:+ +:+:+ +:+  +:+   +:+  :+:+:+  +:+ +:+    +:+ +:+        +:+    +:+
+#+ +:+ +#+ +#+        +#+    +:+ +#+  +:+  +#+ +#+  +:+  +#+ +#++:++#++: +#+ +:+ +#+ +#+    +:+ +#++:++#   +#++:++#: 
+#+  +#+#+# +#+        +#+    +#+ +#+       +#+ +#+       +#+ +#+     +#+ +#+  +#+#+# +#+    +#+ +#+        +#+    +#+
#+#   #+#+# #+#    #+# #+#    #+# #+#       #+# #+#       #+# #+#     #+# #+#   #+#+# #+#    #+# #+#        #+#    #+#
###    ####  ########   ########  ###       ### ###       ### ###     ### ###    #### #########  ########## ###    ###

"""

    

def resize_handler(signum, frame):
    signal_resolver.handle(stdscr)

class HPosEnum(Enum):
    LEFT = 1
    RIGHT = 2
    STRETCH = 3
    AUTO = 4

class VPosEnum(Enum):
    TOP = 1
    BOTTOM = 2
    STRETCH = 3
    AUTO = 4


class Button():
    def __init__(self, title: str):
        self.title = title
        self.realTitle = f"[{self.title}]"
    
    def draw(self, x0):
        # win = curses.newwin(2 , 5, 1, 1)  
        # win.addstr(1, 1, "abc")
        # win.refresh()
        stdscr.addstr(0, x0, self.realTitle) 
    
    def getWidth(self):
        return len(self.realTitle)
    
class HStackPanel():
    def __init__(self, list):
        self.items = list
        
    def addItem(self, item):
        self.items.append(item)

    def draw(self):
        currX = 1
        for item in self.items:
            item.draw(currX)
            currX += item.getWidth() + 1
            
class MyWindow():
    def __init__(self, title: str, x0, y0, x1, y1):
        self.title = title
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
    
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
    def __init__(self, path: str, x0, y0, x1, y1):
        super().__init__(path, x0, y0, x1, y1)
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

    
class MainView():
    def __init__(self, stdscr):
        
        self.windows = []
        self.stdscr = stdscr
    
    def StartQuad(self):
        yMax, xMax = stdscr.getmaxyx()
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
        y0 = 2
        self.windows.append(DirWindow(".", 0, y0, x1, y1))
        self.windows.append(MyWindow("/home/kojaja/", x1, y0, x2, y1))
        self.windows.append(DirWindow(".", 0, y1, x1, y2))
        self.windows.append(DirWindow(".", x1, y1, x2, y2))
        
        self.menuPanel.draw()
        for myWin in self.windows:
            myWin.draw()
        stdscr.refresh()
        
    

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
        lines = hello.splitlines()
        
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
