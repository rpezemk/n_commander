import curses
from curses import endwin
from enum import Enum
import signal
from pathlib import Path
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


class ListHelper():
    @staticmethod
    def group_by_n(input_list, n):
        grouped = []
        for i in range(0, len(input_list), n):
            grouped.append(input_list[i:i + n])
        return grouped

class StringHelper():
    @staticmethod
    def ListToColumns(maxH: int, maxW: int, list):
        groups = ListHelper.group_by_n(list, max(1, maxH))
        nGroups = len(groups)
        if nGroups == 0:
            return []
        
        firstGroupLen = len(groups[0])
        lastGroupLen = len(groups[-1])
        resList = []
        groupWidths = [max([len(s) for s in lst]) + 2 for lst in groups]
        for i in range(lastGroupLen):
            subRes = ""
            subResList = []
            for groupCnt in range(nGroups):
                subResList.append(groups[groupCnt][i])
            
            for groupCnt in range(nGroups):
                subRes += subResList[groupCnt].ljust(groupWidths[groupCnt])
            resList.append(subRes)
            
            
        for i in range(lastGroupLen, firstGroupLen):
            subRes = ""
            subResList = []
            for groupCnt in range(nGroups - 1):
                subResList.append(groups[groupCnt][i])
                
            for groupCnt in range(nGroups - 1):
                subRes += subResList[groupCnt].ljust(groupWidths[groupCnt])
            resList.append(subRes) 
        return resList

class OsHelper():
    @staticmethod
    def get_current_directory():
        current_directory = Path.cwd()  # or Path('.').resolve()
        return current_directory
    
    @staticmethod
    def list_directory_content_scandir(path='.'):
        """
        List the contents of a directory using os.scandir, which is more efficient for large directories.
        
        :param path: Directory path to list the contents of. Default is the current directory.
        :return: List of directory contents.
        """
        corrPath = path
        try:
            if corrPath == ".":
                corrPath = OsHelper.get_current_directory()
            with os.scandir(path) as entries:
                return ([entry.name for entry in entries], corrPath)
        except FileNotFoundError:
            return (f"Directory '{path}' not found.", corrPath)
        except PermissionError:
            return (f"Permission denied to access '{path}'.", corrPath)


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
       
class DirWindow(MyWindow):
    def __init__(self, path: str, x0, y0, x1, y1):
        super().__init__(path, x0, y0, x1, y1)
        self.content, corrPath = OsHelper.list_directory_content_scandir(path)
        self.title = str(corrPath)
        
    def draw(self):
        win = curses.newwin(self.y1 - self.y0,self.x1 - self.x0, self.y0, self.x0)  
        win.border()
        win.addstr(0, 1, self.title)
        content = StringHelper.ListToColumns(self.y1 - self.y0 - 3, self.x1 - self.x0 - 1, self.content)
        for idx, line in enumerate(content):
            if idx > self.y1 - self.y0 - 3:
                break
            win.addstr(1 + idx, 3, line)  
        # for idx, line in enumerate(self.content):
        #     if idx > self.y1 - self.y0 - 3:
        #         break
        #     win.addstr(1 + idx, 3, line)  
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
