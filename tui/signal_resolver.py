import signal
import curses
from curses import endwin

def redraw_stdscreen(stdscr):
    rows, cols = stdscr.getmaxyx()
    stdscr.clear()
    # stdscr.border()
    # stdscr.hline(2, 1, '_', cols-2)
    stdscr.refresh()

def handle(stdscr):
    endwin()
    stdscr.refresh()
    redraw_stdscreen(stdscr)