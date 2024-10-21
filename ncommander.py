import curses
from enum import Enum
from typing import Callable

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

class Drawable():
    def __init__(self):
        pass
    

class Button(Drawable):
    def __init__(self, label: str, onClickFunc: Callable[[], None]):
        pass



class MyWindow():
    def __init__(self):
        pass
    def getContent(self) -> str:
        pass
    def interact(self, ch: int):
        pass
    
class TiledView():
    def __init__(self):
        self.windows = []
    
    def AddWindow(self, win: MyWindow):
        self.windows.add(win)
    
    def StartQuad(self):
        self.windows.add((MyWindow(), HPosEnum.LEFT, VPosEnum.TOP))
        self.windows.add((MyWindow(), HPosEnum.RIGHT, VPosEnum.TOP))
        self.windows.add((MyWindow(), HPosEnum.LEFT, VPosEnum.BOTTOM))
        self.windows.add((MyWindow(), HPosEnum.RIGHT, VPosEnum.BOTTOM))

    def Show(self):
        for w in self.windows:
            pass

class Renderer():
    def __init__(self):
        pass
    
    

def main(stdscr):
    
    stdscr.clear()
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    
    height, width = stdscr.getmaxyx()
    win_height = height - 2
    win_width = width - 2
    win = curses.newwin(win_height, win_width, 1, 1)  

    win.border()

    message = "Hello, Ncurses!"
    y, x = win.getmaxyx()  
    win.addstr(y // 2, (x - len(message)) // 2, message)  

    win.refresh()

    
    win.getch()


curses.wrapper(main)
