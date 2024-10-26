from enum import Enum
import curses
from typing import Callable
from typing import Tuple
from utils import os_utils, string_utils
import os
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

    ITEM_PANEL_COLS_ROWS = 1  # Fill by columns first, then rows
    ITEM_PANEL_ROWS_COLS = 2  # Fill by rows first, then columns


class VisualHierarchy:
    def __init__(
        self,
        parent: "VisualHierarchy",
        children: list["VisualHierarchy"] = None,
        y0: int = 0,
        x0: int = 0,
        y1: int = 0,
        x1: int = 0,
        fillMethod: FillMethod = FillMethod.ITEM_PANEL_ROWS_COLS,
        hPos=HPosEnum.LEFT,
    ):
        self.parent = parent
        if children is None:
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

    def append_child(self, child: "VisualHierarchy"):
        self.children.append(child)
        child.parent = self

    def check_point_belongs(self, x: int, y: int):
        check_h = self.x0 <= x <= self.x1
        check_v = self.y0 <= y <= self.y1
        return check_h and check_v


class Button(VisualHierarchy):
    def __init__(
        self, title: str, parent: VisualHierarchy = None, hPos: HPosEnum = HPosEnum.LEFT
    ):
        super().__init__(parent, hPos=hPos)
        self.title = title
        self.real_title = f"[{self.title}]"

    def draw(self, x0):
        win = curses.newwin(3, len(self.real_title), 0, x0)
        win.addstr(0, 0, self.real_title)
        win.refresh()

    def get_width(self):
        return len(self.real_title)


class ClockButton(Button):
    def __init__(self, title, parent=None, hPos: HPosEnum = HPosEnum.LEFT):
        super().__init__(title, parent, hPos=hPos)

    def draw(self, x0):
        self.real_title = f"[{self.title}]"
        super().draw(x0)

    def update_time(self, time_str: str):
        self.title = time_str


class HStackPanel(VisualHierarchy):
    def __init__(self, list, parent=None, children=[]):
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
    def __init__(
        self,
        title: str,
        parent=None,
        children: list[VisualHierarchy] = [],
        y0=0,
        x0=0,
        y1=0,
        x1=0,
        fillMethod: FillMethod = FillMethod.ITEM_PANEL_ROWS_COLS,
        func: Callable[["MyWindow"], None] = None,
    ):
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
    def __init__(self, title, func: Callable[["MyWindow"], None]):
        super().__init__(
            title, None, [], 0, 0, 0, 0, FillMethod.ITEM_PANEL_ROWS_COLS, func
        )


def fill_window(myWindow: MyWindow) -> None:
    height = myWindow.y1 - myWindow.y0
    width = myWindow.x1 - myWindow.x0
    win = curses.newwin(height, width, myWindow.y0, myWindow.x0)
    win.border()
    win.addstr(0, 1, myWindow.title)
    dirOk, dirs, files, errStr = os_utils.try_get_dir_content(myWindow.title)
    if dirOk:
        content = string_utils.list_to_columns(height - 3, width - 1, dirs + files)
        myWindow.title = os.path.abspath(myWindow.title)
        for idx, line in enumerate(content):
            if idx > myWindow.y1 - myWindow.y0 - 3:
                break
            win.addstr(1 + idx, 3, line)
    else:
        pass
    win.refresh()


class DirPanel(ItemPanel):
    def __init__(self, title):
        super().__init__(title, fill_window)


def fill_log_window(logPanel: "LogPanel") -> None:
    height = logPanel.y1 - logPanel.y0
    width = logPanel.x1 - logPanel.x0
    win = curses.newwin(height, width, logPanel.y0, logPanel.x0)
    win.border()
    win.addstr(0, 1, logPanel.title)
    line_width = width - 3
    max_total_lines = height - 3
    nScrLines = height

    if line_width < 3:
        win.refresh()
        return

    curr_line_no = 0
    last_lines = logPanel.logLines[-max_total_lines:]

    for line in last_lines:
        if curr_line_no > max_total_lines:
            break
        sub_lines = string_utils.split_by_n_chars_other_shorter(
            line, width - 3, width - 7
        )
        if len(sub_lines) == 0:
            continue
        first_sub_line = sub_lines[0][:line_width]
        win.addstr(1 + curr_line_no, 2, first_sub_line)
        curr_line_no += 1

        for sub_line in sub_lines[1:]:
            win.addstr(1 + curr_line_no, 4, "\\ " + sub_line)
            curr_line_no += 1

    win.refresh()


class LogPanel(ItemPanel):
    def __init__(self, title):
        super().__init__(title, fill_log_window)
        self.logLines = []

    def log(self, message):
        d = datetime.now()
        ms = int(d.microsecond / 1000)
        now = d.strftime("%Y-%m-%d %H:%M:%S") + "." + str(ms).rjust(3, "0")
        self.logLines.append(f"[{now}] {message}")


class MainView(VisualHierarchy):
    def __init__(self, stdscr, children=[], menuPanel: HStackPanel = None):
        self.stdscr = stdscr
        yMax, xMax = self.stdscr.getmaxyx()
        super().__init__(
            None, children, 0, 0, yMax, xMax, FillMethod.ITEM_PANEL_ROWS_COLS
        )

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
        y0, x0, y1, x1, y2, x2 = 1, 0, int(self.y1 / 2), int(self.x1 / 2), self.y1, self.x1
        return y0, x0, y1, x1, y2, x2

    def quad_matrix(self, y0, x0, y1, x1, y2, x2):
        matrix = [
            [y0, x0, y1, x1],
            [y0, x1, y1, x2],
            [y1, x0, y2, x1],
            [y1, x1, y2, x2],
        ]
        return matrix

    def set_child_layout(self, ch, y0, x0, y1, x1):
        ch.y0 = y0
        ch.x0 = x0
        ch.y1 = y1
        ch.x1 = x1

    def resolve_mouse_click(self, y0, x0) -> Tuple[bool, VisualHierarchy]:
        pass
