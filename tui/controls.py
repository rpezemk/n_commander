from enum import Enum


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
    
    def appendChild(self, child: 'VisualHierarchy'):
        self.children.append(child)
        child.parent = self
    
    def pointBelongsToThis(self, x: int, y: int):
        checkH = self.x0 <= x <= self.x1
        checkV = self.y0 <= y <= self.y1
        return checkH and checkV