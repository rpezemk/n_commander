import curses
from curses import endwin

class ColorHelper():

    def wrap_color(self, idx: int, fgdColor, bkgColor) -> int:
        curses.init_pair(idx, fgdColor, bkgColor)
        color = curses.color_pair(idx)
        return color
    
    

class MainStyles():
    def __init__(self):
        color_helper = ColorHelper()
        self.red_on_black = color_helper.wrap_color(1, curses.COLOR_RED, curses.COLOR_BLACK)
        self.green_on_black = color_helper.wrap_color(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.yellow_on_black = color_helper.wrap_color(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)