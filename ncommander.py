import curses
from curses import endwin
from enum import Enum
import signal
import os
import time
from typing import Callable
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

class ColorHelper():

    def WrapColor(self, idx: int, fgdColor, bkgColor) -> int:
        curses.init_pair(idx, fgdColor, bkgColor)
        color = curses.color_pair(idx)
        return color
    
    

class MainStyles():
    def __init__(self):
        colorHelper = ColorHelper()
        self.red_on_black = colorHelper.WrapColor(1, curses.COLOR_RED, curses.COLOR_BLACK)
        self.green_on_black = colorHelper.WrapColor(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.yellow_on_black = colorHelper.WrapColor(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
def redraw_stdscreen():
    rows, cols = stdscr.getmaxyx()
    stdscr.clear()
    # stdscr.border()
    # stdscr.hline(2, 1, '_', cols-2)
    stdscr.refresh()

def resize_handler(signum, frame):
    endwin()
    stdscr.refresh()
    redraw_stdscreen()

    
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
        pass
    def draw(self, x0):
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
        self.windows.append(MyWindow("/dev/", 0, y0, x1, y1))
        self.windows.append(MyWindow("/home/kojaja/", x1, y0, x2, y1))
        self.windows.append(MyWindow("/var/", 0, y1, x1, y2))
        self.windows.append(MyWindow("/opt/", x1, y1, x2, y2))
        
        self.menuPanel.draw()
        for myWin in self.windows:
            myWin.draw()
        stdscr.refresh()
        
    

def main(stdscr_local):
    global stdscr
    stdscr = stdscr_local
    signal.signal(signal.SIGWINCH, resize_handler) 
    stdscr_local.clear()
    # curses.mousemask(curses.ALL_MOUSE_EVENTS)
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    yellow_and_blue = curses.color_pair(2)
    styles = MainStyles()
    global helloWashShown
    if not helloWashShown:
        lines = hello.splitlines()
        
        for idx, line in enumerate(lines):
            stdscr.addstr(idx, 2, line, yellow_and_blue)  
            
        stdscr.refresh()  
        stdscr.getch() 
        pass
    helloWashShown = True;
    redraw_stdscreen()
    
    while True:
        tiled = MainView(stdscr_local)
        tiled.StartQuad()
        key = stdscr.getch()
        if key == ord('q'):
            break

     
curses.wrapper(main)
