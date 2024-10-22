import curses

def main(stdscr):
    # Initialize curses color functionality
    if curses.has_colors():
        curses.start_color()
        # Define a color pair with YELLOW text and BLACK background
        curses.init_pair(2, 9, 9)

    # Get the color pair for yellow on black
    yellow_on_black = curses.color_pair(2)

    # Clear the screen and display text with the specified color pair
    stdscr.clear()
    stdscr.addstr(0, 0, "This is yellow text on black background", yellow_on_black)

    # Refresh to show the text on the screen
    stdscr.refresh()
    # Wait for a key press before exiting
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
