import curses

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    
    nColors = int(curses.COLORS/3)
    for i in range(0, nColors):
        fgNo = i
        curses.init_pair(i + 1, fgNo, -1)

    for i in range(0, nColors):
        stdscr.addstr(str(i), curses.color_pair(i + 1))
        # stdscr.getch()
    
    stdscr.addstr("\nlol\n")
    offset = nColors
    for i in range(0, nColors):
        bgNo = i
        curses.init_pair(i + 1 + offset, 0, bgNo)

    for i in range(0, nColors):
        stdscr.addstr(str(i), curses.color_pair(i + 1 + offset))
        # stdscr.getch()
    
    stdscr.getch()
curses.wrapper(main)