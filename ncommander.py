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

        
        
def redraw_stdscreen():
    rows, cols = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.border()
    stdscr.hline(2, 1, '_', cols-2)
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
    
class TiledView():
    def __init__(self, stdscr):
        
        self.windows = []
        self.stdscr = stdscr
    
    def StartQuad(self):
        yMax, xMax = stdscr.getmaxyx()
        x1 = int(xMax/2)
        x2 = xMax 
        y1 = int(yMax/2)
        y2 = yMax
        self.windows.append(MyWindow("/dev/", 0, 0, x1, y1))
        self.windows.append(MyWindow("/home/kojaja/", x1, 0, x2, y1))
        self.windows.append(MyWindow("/var/", 0, y1, x1, y2))
        self.windows.append(MyWindow("/opt/", x1, y1, x2, y2))
        
        for myWin in self.windows:
            win = curses.newwin(myWin.y1 - myWin.y0,myWin.x1 - myWin.x0, myWin.y0, myWin.x0)  
            win.border()
            win.addstr(0, 1, myWin.title)
            win.refresh()
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
    redraw_stdscreen()
    
    global helloWashShown
    if not helloWashShown:
        lines = hello.splitlines()
        for idx, line in enumerate(lines):
            stdscr.addstr(idx, 2, line)  
            
        stdscr.refresh()  
        stdscr.getch() 
        pass
    helloWashShown = True;
    
    while True:
        tiled = TiledView(stdscr_local)
        tiled.StartQuad()
        key = stdscr.getch()
        if key == ord('q'):
            break

     
curses.wrapper(main)
