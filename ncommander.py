import curses
import os
from utils import os_utils, string_utils
import asyncio
from datetime import datetime
from tui import signal_resolver
from tui.pzgrid import VisualGrid
from tui.measures import Area, Segment, Len, LenT
from tui.placements import GPlace
from tui.text_box import TextBox

from tui.controls import (
    Button, ClockButton, HStackPanel,
    DirPanel, VisualHierarchy
)

from tui.placements import PPlace, VPosEnum, HPosEnum


###### GUI ELEMENTS ######
app_is_running = True
vg: VisualGrid = None 

clock = ClockButton("", p_place=PPlace(hPos=HPosEnum.RIGHT))

menu = HStackPanel(None, 
        children= [Button("edit"), Button("view"), Button("settings"),
                   Button("help"), Button("about"), clock], 
        g_place=GPlace(0, 1, 0, 2)
    )


log_panel = TextBox("[LOGGER]")
log_panel.g_place = GPlace(1, 1, 1, 1)

row_defs = [Len(1, LenT.ABS), Len(50, LenT.STAR), Len(50, LenT.STAR)]
col_defs = [Len(50, LenT.STAR), Len(50, LenT.STAR)]

vg_children = [
    menu,
    DirPanel(os.path.abspath("."), g_plc=GPlace(1, 1, 0, 1)),
    log_panel,
    DirPanel(os.path.abspath("."), g_plc=GPlace(2, 1, 0, 1)),
    DirPanel(os.path.abspath("."), g_plc=GPlace(2, 1, 1, 1)),
    ]


async def resolve_input_continous(stdscr, log_panel: TextBox, vg: VisualHierarchy = None):
    global app_is_running
    if log_panel is None:
        while app_is_running:
            await asyncio.sleep(0.01)
            
    while app_is_running:
        key = stdscr.getch()
        if key == -1:
            pass
        elif key == curses.KEY_MOUSE:
            id, mx, my, mz, bs = curses.getmouse()
            log_panel.log(f"M: k:{key}, bs:{bs} ({my}, {mx}, {mz})")
            # (mx, my)
            all_belonging = [x for x in vg.get_all_objects() if x.check_point_belongs(mx, my)]
            for obj in all_belonging:
                log_panel.log(f"{obj.area.y0}, {obj.area.x0}, {obj.area.y1}, {obj.area.x1},   {obj.get_name()}")
        elif key == ord("q"):
            app_is_running = False
        else:
            log_panel.log(f"K: k:{key}")
        
        await asyncio.sleep(0.01)




async def async_grid_refresh(grid: VisualGrid):
    while app_is_running:
        grid.draw()
        await asyncio.sleep(0.1)
        
async def async_slow_refresh():
    while app_is_running:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clock.set_time(now)
        await asyncio.sleep(0.1)
        

async def run_async_tasks(stdscr):
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    stdscr.nodelay(True)  # Non-blocking mode
    global vg
    vg = VisualGrid(None, vg_children, row_defs=row_defs, col_defs=col_defs, stdscr=stdscr)
    slow_task = asyncio.create_task(async_slow_refresh())
    input_task = asyncio.create_task(resolve_input_continous(stdscr, log_panel, vg))
    tui_task = asyncio.create_task(async_grid_refresh(vg))
    await tui_task
    stdscr.clear()
    stdscr.refresh()
    
def main(stdscr):
    signal_resolver.init_screen(stdscr)
    asyncio.run(run_async_tasks(stdscr))


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"Error: {e}")

