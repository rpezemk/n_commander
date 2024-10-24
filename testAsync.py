import curses
import time
import threading

class Clock:
    def __init__(self):
        self.running = True

    def start(self):
        while self.running:
            self.update()
            time.sleep(0.1)  # Wait for 100 ms

    def update(self):
        # Get the current time
        now = time.strftime("%H:%M:%S") + f".{int((time.time() % 1) * 1000):03d}"
        print(f"Current Time: {now}")  # Print to the console

    def stop(self):
        self.running = False

def main(stdscr):
    # Clear screen and prepare for the clock display
    stdscr.clear()
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Set getch() to non-blocking
    stdscr.timeout(100) # Set a timeout for getch()

    # Create an instance of the Clock class
    clock = Clock()
    
    # Start the clock thread
    clock_thread = threading.Thread(target=clock.start)
    clock_thread.start()

    try:
        while True:
            # Display text on the curses screen
            stdscr.clear()
            stdscr.addstr(0, 0, "Press 'q' to exit...", curses.A_BOLD)
            stdscr.refresh()

            # Check for user input
            key = stdscr.getch()
            if key == ord('q'):  # Press 'q' to exit
                break
            curses.napms(10)  # Short nap to prevent busy waiting
    finally:
        # Stop the clock thread cleanly
        clock.stop()
        clock_thread.join()  # Wait for the thread to finish

if __name__ == "__main__":
    # Start the curses application
    curses.wrapper(main)
