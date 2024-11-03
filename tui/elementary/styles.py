import curses
from dataclasses import dataclass

splash_content = """
::::    :::  ::::::::   ::::::::  ::::    ::::  ::::    ::::      :::     ::::    ::: :::::::::  :::::::::: ::::::::: 
:+:+:   :+: :+:    :+: :+:    :+: +:+:+: :+:+:+ +:+:+: :+:+:+   :+: :+:   :+:+:   :+: :+:    :+: :+:        :+:    :+:
:+:+:+  +:+ +:+        +:+    +:+ +:+ +:+:+ +:+ +:+ +:+:+ +:+  +:+   +:+  :+:+:+  +:+ +:+    +:+ +:+        +:+    +:+
+#+ +:+ +#+ +#+        +#+    +:+ +#+  +:+  +#+ +#+  +:+  +#+ +#++:++#++: +#+ +:+ +#+ +#+    +:+ +#++:++#   +#++:++#: 
+#+  +#+#+# +#+        +#+    +#+ +#+       +#+ +#+       +#+ +#+     +#+ +#+  +#+#+# +#+    +#+ +#+        +#+    +#+
#+#   #+#+# #+#    #+# #+#    #+# #+#       #+# #+#       #+# #+#     #+# #+#   #+#+# #+#    #+# #+#        #+#    #+#
###    ####  ########   ########  ###       ### ###       ### ###     ### ###    #### #########  ########## ###    ###
"""
# splash_content = """
# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_-+abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY
# """


@dataclass
class MainStyles:
    @classmethod
    def initialize(cls):
        transp = -1
        # Initialize color pairs
        # Normal
        cls.red = cls.wrap_color(curses.COLOR_RED, transp)
        cls.green = cls.wrap_color(curses.COLOR_GREEN, transp)
        cls.blue = cls.wrap_color(curses.COLOR_BLUE, transp)
        cls.yellow = cls.wrap_color(curses.COLOR_YELLOW, transp)
        cls.cyan = cls.wrap_color(curses.COLOR_CYAN, transp)
        cls.magenta = cls.wrap_color(curses.COLOR_MAGENTA, transp)

        cls.white = cls.wrap_color(curses.COLOR_WHITE, transp)

        # Inverted
        cls.red_inv = cls.wrap_color(transp, curses.COLOR_RED)
        cls.green_inv = cls.wrap_color(transp, curses.COLOR_GREEN)
        cls.blue_inv = cls.wrap_color(transp, curses.COLOR_BLUE)
        cls.yellow_inv = cls.wrap_color(transp, curses.COLOR_YELLOW)
        cls.cyan_inv = cls.wrap_color(transp, curses.COLOR_CYAN)
        cls.magenta_inv = cls.wrap_color(transp, curses.COLOR_MAGENTA)

        cls.white_inv = cls.wrap_color(transp, curses.COLOR_WHITE)

        cls.crazy = []
        cls.currNo += 5
        nColors = 100

        for colorNo in range(0, nColors):
            cls.crazy += [cls.wrap_color(transp, colorNo)]
            pass
        # for colorNo in range(0, nColors):
        #     cls.crazy += [cls.wrap_color(colorNo, transp)]
        #     pass

    currNo = 1

    @classmethod
    def wrap_color(cls, fgdColor: int, bkgColor: int) -> int:
        """Wrap the color pair initialization."""
        nColors = curses.COLORS
        curses.init_pair(cls.currNo, fgdColor, bkgColor)
        resColor = curses.color_pair(cls.currNo)
        cls.currNo += 1
        return resColor


def main(stdscr):
    # Clear the screen
    stdscr.clear()

    # Start color functionality
    curses.start_color()
    curses.use_default_colors()  # Allow use of default terminal colors
    MainStyles.initialize()
    # stdscr.addstr(0, 0, "Normal Colors:", MainStyles.red)
    # stdscr.addstr(1, 0, "Normal Colors:", MainStyles.green)
    # stdscr.addstr(2, 0, "Normal Colors:", MainStyles.yellow)
    # stdscr.addstr(3, 0, "Normal Colors:", MainStyles.white)
    # stdscr.addstr(4, 0, "Normal Colors:", MainStyles.cyan)
    # stdscr.addstr(5, 0, "Normal Colors:", MainStyles.magenta)

    # stdscr.addstr(7, 0, "Inverted Colors:", MainStyles.red_inv)
    # stdscr.addstr(8, 0, "Inverted Colors:", MainStyles.green_inv)
    # stdscr.addstr(9, 0, "Inverted Colors:", MainStyles.yellow_inv)
    # stdscr.addstr(10, 0, "Inverted Colors:", MainStyles.white_inv)
    # stdscr.addstr(11, 0, "Inverted Colors:", MainStyles.cyan_inv)
    # stdscr.addstr(12, 0, "Inverted Colors:", MainStyles.magenta_inv)

    palette = MainStyles.crazy
    palLen = len(palette)
    lines = splash_content.splitlines()
    stdscr.timeout(10)
    width = max([len(l) for l in lines])
    for iter in range(0, 10000):
        for lineNo, line in enumerate(lines):
            for colNo in range(0, min(width, len(line))):
                currColor = palette[(colNo + iter) % palLen]
                stdscr.addstr(lineNo, colNo, line[colNo], currColor)
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord("q"):  # If 'q' is pressed
            break

    # Refresh the screen to show the text
    stdscr.refresh()

    # Wait for user input
    MainStyles.initialize()
    stdscr.getch()


curses.wrapper(main)
