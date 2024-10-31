import os
from pathlib import Path
import curses
from enum import Enum
from datetime import datetime
from typing import Callable, Tuple

from utils import os_utils, string_utils
from tui.placements import GPlace, HPosEnum, PPlace
from tui.measures import Area
from tui.base_visual import BaseVisual


class Btn(BaseVisual):
    def __init__(
        self, title: str, parent: BaseVisual = None,
            g_place: GPlace = None, 
            p_place: PPlace = PPlace()
    ):
        super().__init__(parent, [], Area(), g_place, p_place)
        self.title = title
        self.real_title = f"[{self.title}]"

    def draw(self):
        n_win = self.emit_window()
        n_win.addstr(0, 0, self.real_title)

    def get_width(self):
        return len(self.real_title)
    
    def get_dims(self):
        self.area.x1 = self.area.x0 + len(self.real_title)
        self.area.y1 = self.area.y0
        return self.area.get_dims()


class Clock(Btn):
    def __init__(self, parent=None,
                g_place: GPlace = None, 
                p_place: PPlace = PPlace()):
        self.title = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.real_title = f"[{self.title}]"
        super().__init__(self.title, parent, g_place, p_place)

    def draw(self):
        self.title = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.real_title = f"[{self.title}]"
        super().draw()
        
    def get_width(self):
        return len(self.real_title)

class HPanel(BaseVisual):
    def __init__(self, parent=None, children=[],
            g_place: GPlace = None, 
            p_place: PPlace = PPlace()):
        super().__init__(parent, children, p_place=p_place, g_place=g_place)

    def draw(self):
        curr_x_left = 1
        curr_x_right = self.area.x1 + 1
        for item in self.children:
            if item.p_place.hPos == HPosEnum.LEFT:
                item.area.x0 = curr_x_left
                curr_x_left += item.get_width() + 1
            if item.p_place.hPos == HPosEnum.RIGHT:
                curr_x_right -= item.get_width()
                item.area.x0 = curr_x_right
            item.draw()


class Panel(BaseVisual):
    def __init__(
        self,
        title: str,
        parent=None,
        children: list[BaseVisual] = [],
        area: Area = Area(),
        g_place: GPlace = None, 
        p_place: PPlace = PPlace()
    ):
        super().__init__(parent, children, area, g_place=g_place, p_place=p_place)
        self.title = title

    def draw(self):
        ...

class DirP(Panel):
    def __init__(self, title = None,
                    g_plc: GPlace = None, 
                    p_place: PPlace = PPlace()
                    ):
        absolute_path = title
        if absolute_path is None or title == '' or title == '.':
            absolute_path = str(Path(".").resolve())
        super().__init__(absolute_path, g_place=g_plc, p_place=p_place)

    def draw(self) -> None:
        h, w = self.get_dims()
        if h < 1:
            return
        win = self.emit_window().draw_border()
        win.addstr(0, 1, self.title)
        dirOk, dirs, files, errStr = os_utils.try_get_dir_content(self.title)
        if dirOk and h - 3 > 0:
            content = string_utils.list_to_columns(h - 3, w - 2, dirs + files)
            for idx, line in enumerate(content):
                if idx <= h - 3:
                    win.addstr(1 + idx, 3, line)
                    ...


               
