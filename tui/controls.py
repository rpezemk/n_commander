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
            grid_placement: GPlace = None, 
            panel_placement: PPlace = PPlace()
    ):
        super().__init__(parent, [], Area(), grid_placement, panel_placement)
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
                grid_placement: GPlace = None, 
                panel_placement: PPlace = PPlace()):
        super().__init__(title, parent, grid_placement, panel_placement)

    def draw(self):
        self.real_title = f"[{self.title}]"
        super().draw()

    def set_time(self, time_str: str):
        self.title = time_str


class HStackPanel(VisualHierarchy):
    def __init__(self, parent=None, children=[],
            grid_placement: GPlace = None, 
            panel_placement: PPlace = PPlace()):
        super().__init__(parent, children, panel_placement=panel_placement, grid_placement=grid_placement)

    def draw(self):
        curr_x_left = 1
        curr_x_right = self.area.x1
        for item in self.children:
            if item.panel_placement.hPos == HPosEnum.LEFT:
                item.area.x0 = curr_x_left
                curr_x_left += item.get_width() + 1
            if item.panel_placement.hPos == HPosEnum.RIGHT:
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
        grid_placement: GPlace = None, 
        panel_placement: PPlace = PPlace(),
        func: Callable[["Panel"], None] = None,
    ):
        super().__init__(parent, children, area, grid_placement=grid_placement, panel_placement=panel_placement)
        self.title = title
        self.func = func

    def draw(self):
        if self.func:
            self.func(self)


class ItemPanel(Panel):
    def __init__(self, title, func: Callable[["Panel"], None],
                    grid_placement: GPlace = None, 
                    panel_placement: PPlace = PPlace(),
                 ):
        super().__init__(
            title, None, [], Area(), panel_placement=panel_placement, grid_placement=grid_placement, func=func
        )

class DirPanel(ItemPanel):
    def __init__(self, title,
                    g_plc: GPlace = None, 
                    panel_placement: PPlace = PPlace()
                    ):
        super().__init__(title, self.fill_window, grid_placement=g_plc, panel_placement=panel_placement)

    def fill_window(self, myWindow: Panel) -> None:
        h, w = myWindow.area.get_dims()
        win = curses.newwin(h, w, myWindow.area.y0, myWindow.area.x0)
        win.border()
        win.addstr(0, 1, myWindow.title)
        dirOk, dirs, files, errStr = os_utils.try_get_dir_content(myWindow.title)
        if dirOk:
            content = string_utils.list_to_columns(h - 2, w - 1, dirs + files)
            for idx, line in enumerate(content):
                if idx <= h - 2:
                    win.addstr(1 + idx, 3, line)
        win.refresh()
        
        
class LogPanel(ItemPanel):
    def __init__(self, title):
        super().__init__(title, self.fill_log_window)
        self.logLines = []
        
    def log(self, message):
        d = datetime.now()
        ms = int(d.microsecond / 1000)
        now = d.strftime("%Y-%m-%d %H:%M:%S") + "." + str(ms).rjust(3, "0")
        self.logLines.append(f"[{now}] {message}")
  
    def fill_log_window(self, logPanel: "LogPanel") -> None:
        h, w = logPanel.area.get_dims()
        win = curses.newwin(h, w, logPanel.area.y0, logPanel.area.x0)
        win.border()
        win.addstr(0, 1, logPanel.title)
        line_width = w - 3
        v_capacity = h - 2

        if line_width < 1:
            win.refresh()
            return
        
        curr_line_no = 0
        last_lines = logPanel.logLines[-v_capacity:]

        for line in last_lines:
            if curr_line_no > v_capacity:
                break
            sub_lines = string_utils.split_by_n_chars_other_shorter(line, w - 3, w - 7)
            if len(sub_lines) == 0:
                continue
            first_sub_line = sub_lines[0][:line_width]
            win.addstr(1 + curr_line_no, 2, first_sub_line)
            curr_line_no += 1

            for sub_line in sub_lines[1:]:
                win.addstr(1 + curr_line_no, 4, "\\ " + sub_line)
                curr_line_no += 1
        win.refresh()
