import sys,os
import curses

def clip(i: int, min: int, max: int) -> int:
    x = min(max, max(min, x))  
    return x
    

def draw_menu(stdscr):

    # Clear screen
    stdscr.clear()
    
    k = 0
    x = 0
    y = 0

    stdscr.clear()
    stdscr.refresh()
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        
        stdscr.bkgd(' ', curses.color_pair(0))
    abc = "TEST"
    stdscr.addstr(12, 12, abc, curses.color_pair(1))

    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            y = y + 1
        elif k == curses.KEY_UP:
            y = y - 1
        elif k == curses.KEY_RIGHT:
            x = x + 1
        elif k == curses.KEY_LEFT:
            x = x - 1

        x = max(0, x)
        x = min(width-1, x)

        y = max(0, y)
        y = min(height-1, y)

        title = "Curses example"[:width-1]
        subtitle = "ABC ABC"[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(x, y)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(y, x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
