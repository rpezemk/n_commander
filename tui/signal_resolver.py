import signal
import curses
from curses import endwin

stdscr = None


def resize_handler(signum, frame):
    handle(stdscr)

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
    
    
def init_screen(scr):
    signal.signal(signal.SIGWINCH, resize_handler) 
    global stdscr
    stdscr = scr
    stdscr.clear()
    redraw_stdscreen(stdscr)
    # curses.mousemask(curses.ALL_MOUSE_EVENTS)
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        