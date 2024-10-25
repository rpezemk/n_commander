import curses

# Global variable for running state
app_is_running = True


def resolve_input(stdscr, log_panel):
    global app_is_running

    # Enable mouse events
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    stdscr.nodelay(True)  # Non-blocking mode

    # Main input handling loop
    while app_is_running:
        key = stdscr.getch()

        # No key pressed
        if key == -1:
            continue

        # Mouse event handling
        if key == curses.KEY_MOUSE:
            try:
                _, mx, my, _, button_state = curses.getmouse()
                log_panel.log(f"KBD: got {key} key")

                if (
                    button_state & curses.BUTTON1_CLICKED
                    or button_state & curses.BUTTON3_CLICKED
                ):
                    log_panel.log(f"KBD: Mouse clicked at ({my}, {mx})")

            except curses.error:
                log_panel.log("KBD: Error reading mouse event")

        # Quit on 'q' key
        if key == ord("q"):
            app_is_running = False


# Example dummy log panel for testing
class LogPanel:
    def log(self, message):
        print(message)  # Replace with actual log display in your app


def main(stdscr):
    global app_is_running
    log_panel = LogPanel()
    resolve_input(stdscr, log_panel)


curses.wrapper(main)
