from tui.base_visual import BaseVisual
from tui.elementary.measures import Area
import tui.elementary.special_chars

from typing import Callable, Tuple

class HProgressBar(BaseVisual):
    def __init__(self, parent, children = None, area = ..., g_place = None, p_place = ...,
                 max_val: float = 100, get_val_func: Callable[[], float] = None):
        super().__init__(parent, children, area, g_place, p_place)
        self.max_val = max_val
        self.get_val_func = get_val_func
        
        
    def draw(self):
        h, w = self.area.get_dims()
        if self.get_val_func is None or w - 2 < 0:
            return
        
        y0, x0 = self.area.y0, self.area.x0
        val = self.get_val_func()
        bar_str = "*" + tui.elementary.special_chars.get_h_bar(w - 2, self.max_val, val) + "*"
        win = self.emit_window()
        win.addstr(0, 0, bar_str)
        

class VProgressBar(BaseVisual):
    def __init__(self, parent, children = None, area = ..., g_place = None, p_place = ...,
                 max_val: float = 100, get_val_func: Callable[[], float] = None):
        super().__init__(parent, children, Area(), g_place, p_place)
        self.max_val = max_val
        self.get_val_func = get_val_func
    
    def get_width(self):
        return 0
        
    def draw(self):
        h, w = self.area.get_dims()
        if self.get_val_func is None or w < 0:
            return
        
        y0, x0 = self.area.y0, self.area.x0
        val = self.get_val_func()
        bar_str = "*" + tui.elementary.special_chars.get_v_bar(h - 2, self.max_val, val) + "*"
        win = self.emit_window()
        max_idx = len(bar_str) - 1
        for idx, ch in enumerate(bar_str):
            win.addstr(max_idx - idx, 0, ch)