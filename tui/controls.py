from enum import Enum
import curses
from typing import Callable
from datetime import datetime

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
                 fillMethod: FillMethod = FillMethod.ITEM_PANEL_ROWS_COLS, hPos = HPosEnum.LEFT):
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
        self.hPos = hPos
        
    def append_child(self, child: 'VisualHierarchy'):
        self.children.append(child)
        child.parent = self
    
    def check_point_belongs(self, x: int, y: int):
        check_h = self.x0 <= x <= self.x1
        check_v = self.y0 <= y <= self.y1
        return check_h and check_v
    
    
    
class Button(VisualHierarchy):
    def __init__(self, title: str, parent = None, hPos = HPosEnum.LEFT):
        super().__init__(parent, hPos= hPos)
        self.title = title
        self.real_title = f"[{self.title}]"
        
    def draw(self, x0):
        win = curses.newwin(3 , len(self.real_title), 0, x0)  
        win.addstr(0, 0, self.real_title)
        win.refresh()

    def get_width(self):
        return len(self.real_title)



    
class HStackPanel(VisualHierarchy):
    def __init__(self, list, parent = None, children = []):
        super().__init__(parent, children)
        self.items = list
        
    def addItem(self, item):
        self.items.append(item)

    def draw(self):
        curr_x_left = 1
        curr_x_right = self.x1
        
        for item in self.items:
            if item.hPos == HPosEnum.LEFT:
                item.draw(curr_x_left)
                curr_x_left += item.get_width() + 1
            if item.hPos == HPosEnum.RIGHT:
                curr_x_right -= item.get_width()
                item.draw(curr_x_right)
                
            
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
        
    def draw(self):
        if self.func:
            self.func(self)
     
class ItemPanel(MyWindow):
    def __init__(self, title, func: Callable[['MyWindow'], None]):
        super().__init__(title, None, [], 0, 0, 0, 0, FillMethod.ITEM_PANEL_ROWS_COLS, func)

   
class MainView(VisualHierarchy):
    def __init__(self, stdscr, children = [], 
                 menuPanel: HStackPanel = None):
        self.stdscr = stdscr
        yMax, xMax = self.stdscr.getmaxyx()
        super().__init__(None, children, 0, 0, yMax, xMax, FillMethod.ITEM_PANEL_ROWS_COLS)

        self.stdscr = stdscr
        self.menu_panel = menuPanel
    
    def refresh_quad(self):
        pts = self.get_quad_points()
        
        m = self.quad_matrix(*pts)
        self.set_child_layout(self.children[0], *m[0])
        self.set_child_layout(self.children[1], *m[1]) 
        self.set_child_layout(self.children[2], *m[2])
        self.set_child_layout(self.children[3], *m[3]) 
        self.menu_panel.x1 = self.x1
        self.menu_panel.y1 = 0
        self.menu_panel.draw()
        
        for myWin in self.children:
            myWin.draw()
            
    def get_quad_points(self):
        self.y1, self.x1 = self.stdscr.getmaxyx()
        x0 = 0
        y0 = 1
        yMax, xMax = (self.y1, self.x1)
        x1 = int(xMax/2)
        x2 = xMax 
        y1 = int(yMax/2)
        y2 = yMax
        
        return [y0, x0, y1, x1, y2, x2]
        
    def quad_matrix(self, y0, x0, y1, x1, y2, x2):
        matrix = [[y0, x0, y1, x1],
                  [y0, x1, y1, x2],
                  [y1, x0, y2, x1],
                  [y1, x1, y2, x2]]
        return matrix
        
    def set_child_layout(self, ch, y0, x0, y1, x1):
        ch.y0 = y0
        ch.x0 = x0
        ch.y1 = y1
        ch.x1 = x1
