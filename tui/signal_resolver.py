import signal
import curses
from curses import endwin

stdscr = None


def resize_handler(signum, frame):
    handle(stdscr)

def redraw_stdscreen(stdscr):
    stdscr.clear()
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
        