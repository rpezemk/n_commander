import os
import curses
from enum import Enum
from datetime import datetime
from typing import Callable, Tuple
from utils import os_utils, string_utils
from tui.placements import GPlace, HPosEnum, PPlace
from tui.measures import Area
from tui.visual_hierarchy import VisualHierarchy


class Button(VisualHierarchy):
    def __init__(
        self, title: str, parent: VisualHierarchy = None,
            g_place: GPlace = None, 
            p_place: PPlace = PPlace()
    ):
        super().__init__(parent, [], Area(), g_place, p_place)
        self.title = title
        self.real_title = f"[{self.title}]"

    def draw(self):
        win = curses.newwin(3, len(self.real_title), 0, self.area.x0)
        win.addstr(0, 0, self.real_title)
        win.refresh()

    def get_width(self):
        return len(self.real_title)


class ClockButton(Button):
    def __init__(self, title, parent=None,
                g_place: GPlace = None, 
                p_place: PPlace = PPlace()):
        super().__init__(title, parent, g_place, p_place)

    def draw(self):
        self.real_title = f"[{self.title}]"
        super().draw()

    def set_time(self, time_str: str):
        self.title = time_str


class HStackPanel(VisualHierarchy):
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


class Panel(VisualHierarchy):
    def __init__(
        self,
        title: str,
        parent=None,
        children: list[VisualHierarchy] = [],
        area: Area = Area(),
        g_place: GPlace = None, 
        p_place: PPlace = PPlace()
    ):
        super().__init__(parent, children, area, g_place=g_place, p_place=p_place)
        self.title = title

    def draw(self):
        ...

class DirPanel(Panel):
    def __init__(self, title,
                    g_plc: GPlace = None, 
                    p_place: PPlace = PPlace()
                    ):
        super().__init__(title, g_place=g_plc, p_place=p_place)

    def draw(self) -> None:
        h, w = self.area.get_dims()
        if h < 1:
            return
        win = self.emit_window()
        
        dirOk, dirs, files, errStr = os_utils.try_get_dir_content(self.title)
        if dirOk and h - 2 > 0:
            content = string_utils.list_to_columns(h - 2, w - 1, dirs + files)
            for idx, line in enumerate(content):
                if idx <= h - 2:
                    win.addstr(1 + idx, 3, line)
                    ...
        win.refresh()

               
