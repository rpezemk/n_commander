from enum import Enum
import curses
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
    
class FillMethod(Enum):
    """Fill methods

    Args:
        Enum (FillMethod): methods of filling window
    """     
    ITEM_PANEL_COLS_ROWS = 1 # Fill by columns first, then rows
    ITEM_PANEL_ROWS_COLS = 2 # Fill by rows first, then columns
    

class VisualHierarchy():
    def __init__(self, parent: 'VisualHierarchy', children: list['VisualHierarchy'] = None, 
                 y0 = 0, x0 = 0, y1: int = 0, x1: int = 0, 
                 fillMethod: FillMethod = FillMethod.ITEM_PANEL_ROWS_COLS):
        self.parent = parent
        if children == None:
            self.children = []
        else:
            self.children = children
            for child in children:
                child.parent = self
                
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1
    
    def append_child(self, child: 'VisualHierarchy'):
        self.children.append(child)
        child.parent = self
    
    def check_point_belongs(self, x: int, y: int):
        check_h = self.x0 <= x <= self.x1
        check_v = self.y0 <= y <= self.y1
        return check_h and check_v
    
    
    
class Button(VisualHierarchy):
    def __init__(self, title: str, parent = None):
        super().__init__(parent)
        self.title = title
        self.real_title = f"[{self.title}]"
        
    def draw(self, x0):
        win = curses.newwin(3 , len(self.real_title), 0, x0)  
        win.addstr(0, 0, self.real_title)
        win.refresh()

    def getWidth(self):
        return len(self.real_title)
    
    
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
    def __init__(self, title: str, parent = None, children = [], 
                 y0 = 0, x0 = 0, y1 = 0, x1 = 0, 
                 fillMethod: FillMethod = FillMethod.ITEM_PANEL_ROWS_COLS,
                 func: Callable[['MyWindow'], None] = None):
        super().__init__(parent, children, y0, x0, y1, x1, fillMethod)
        self.title = title
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.func = func
        # self.contentFunc = contentFunc
    
    def getContent(self) -> str:
        pass
    
    def interact(self, ch: int):
        pass
    
    def draw(self):
        self.func(self)
        
class QuadView(VisualHierarchy):
    def __init__(self, stdscr, parent = None, children = [], 
                 y0 = 0, x0 = 0, y1: int = 0, x1: int = 0, 
                 fillMethod: FillMethod = FillMethod.ITEM_PANEL_ROWS_COLS, menuPanel: HStackPanel = None):
        
        super().__init__(parent, children, y0, x0, y1, x1, fillMethod)
        self.stdscr = stdscr
        self.menu_panel = menuPanel
        
    def start_quad(self):                         
        self.menu_panel.draw()
        for myWin in self.children:
            myWin.draw()
        self.stdscr.refresh()