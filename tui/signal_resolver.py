import signal
import curses
from curses import endwin

splash_content = """
·································································································
:       .x+=:.                                            ..                        ..          :
:      z`    ^%                                     x .d88"                       dF            :
:         .   <k                          .u    .    5888R                       '88bu.         :
:       .@8Ned8"       .         u      .d88B :@8c   '888R                 .u    '*88888bu      :
:     .@^%8888"   .udR88N     us888u.  ="8888f8888r   888R              ud8888.    ^"*8888N     :
:    x88:  `)8b. <888'888k .@88 "8888"   4888>'88"    888R            :888'8888.  beWE "888L    :
:    8888N=*8888 9888 'Y"  9888  9888    4888> '      888R            d888 '88%"  888E  888E    :
:     %8"    R88 9888      9888  9888    4888>        888R            8888.+"     888E  888E    :
:      @8Wou 9%  9888      9888  9888   .d888L .+     888R   88888888 8888L       888E  888F    :
:    .888888P`   ?8888u../ 9888  9888   ^"8888*"     .888B . 88888888 '8888c. .+ .888N..888     :
:    `   ^"F      "8888P'  "888*""888"     "Y"       ^*888%            "88888%    `"888*""      :
:                   "P'     ^Y"   ^Y'                  "%                "YP'        ""         :
·································································································
"""

hello_was_shown = False;
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
    
    global hello_was_shown
    if not hello_was_shown:
        lines = splash_content.splitlines()
        
        for idx, line in enumerate(lines):
            stdscr.addstr(idx, 2, line)  
            
        stdscr.refresh()  
        stdscr.getch() 
        pass
    
    # 10 Hz refresh rate
    stdscr.timeout(100)
    hello_was_shown = True;
    stdscr.nodelay(True)  
    stdscr.clear()