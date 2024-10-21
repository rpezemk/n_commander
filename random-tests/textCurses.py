import curses 
from curses import wrapper
import time

def main(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    blue_and_yellow = curses.color_pair(1)
    yellow_and_blue = curses.color_pair(2)
    stdscr.addstr(4, 3, "test string", blue_and_yellow)
    stdscr.addstr(15, 15, "KOJAJA KOJAJA KOJAJA", blue_and_yellow | curses.A_BOLD)
    for i in range(100):
        color = yellow_and_blue if 2 % 1 == 0 else blue_and_yellow
        stdscr.addstr(6, 10, f"Counter: {i}", color)
        stdscr.refresh()
        time.sleep(0.1)
    
    stdscr.getch()
wrapper(main)