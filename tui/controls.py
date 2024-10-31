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


class DirBtn(Btn):
    def __init__(self, title, parent = None, g_place = None, p_place = PPlace()):
        super().__init__(title, parent, g_place, p_place)
    
    def click(self):
        return super().click()

class FileBtn(Btn):
    def __init__(self, title, parent = None, g_place = None, p_place = PPlace()):
        super().__init__(title, parent, g_place, p_place)
        self.real_title = self.title
    def click(self):
        return super().click()

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
        height, width = self.get_dims()
        win = self.emit_window().draw_border()
        win.addstr(0, 1, self.title)
        if height < 3:
            return
        dirOk, dirs, files, errStr = os_utils.try_get_dir_content(self.title)
        
        self.children = [*list([DirBtn(dir) for dir in dirs]), *list([FileBtn(file) for file in files])]
        y0 = 1 + self.area.y0 
        x0 = self.area.x0 + 2
        prev_x_offset = 0
        children_to_draw = []
        ch_groups = string_utils.group_elements_by_n(self.children, height - 2)
        n_groups = len(ch_groups)
        for idx, ch_group in enumerate(ch_groups):
            for idx, ch in enumerate(ch_group):    
                y_offset = y0 + (idx % (height - 2))
                child_len = len(ch.real_title)
                ch.area = Area(y_offset, x0, y_offset, x0 + child_len)
                children_to_draw.append(ch)
            
            if x0 > width:
                break
            x0 += max([len(ch.real_title) for ch in ch_group]) + 1    
            ...
        for ch in children_to_draw:
            ch.draw()
        # for ch in self.children:
        #     ch.draw()
