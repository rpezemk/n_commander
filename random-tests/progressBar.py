import asyncio
import curses

async def draw_progress_bar(stdscr, progress, total):
    stdscr.clear()  # Clear the screen
    height, width = stdscr.getmaxyx()  # Get dimensions of the window

    # Calculate the progress percentage
    percentage = progress / total
    bar_length = int(width * 0.8)  # Length of the progress bar

    # Calculate the filled length of the progress bar
    filled_length = int(bar_length * percentage)
    
    # Create the progress bar string
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    # Display the progress bar
    stdscr.addstr(height // 2, (width - bar_length) // 2, bar)
    stdscr.addstr(height // 2 + 1, (width - 20) // 2, f'Progress: {progress}/{total} ({percentage:.2%})')
    stdscr.refresh()  # Refresh the screen

async def timer_task(total, interval, update_event):
    progress = 0
    while progress < total:
        await asyncio.sleep(interval)  # Wait for the specified interval
        progress += 1
        update_event.set()  # Signal that progress has been updated

async def main(stdscr):
    total = 100  # Total number of iterations
    interval = 0.1  # Interval for the timer in seconds
    update_event = asyncio.Event()  # Event to signal progress updates

    # Start the timer task
    asyncio.create_task(timer_task(total, interval, update_event))

    progress = 0
    while progress <= total:
        await update_event.wait()  # Wait for the update event to be set
        update_event.clear()  # Clear the event flag

        await draw_progress_bar(stdscr, progress, total)
        progress += 1  # Update progress

if __name__ == "__main__":
    curses.wrapper(lambda stdscr: asyncio.run(main(stdscr)))
