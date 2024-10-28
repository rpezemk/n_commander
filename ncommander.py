import curses
import os
from pathlib import Path
from datetime import datetime
import asyncio

from utils import os_utils, string_utils
from tui import signal_resolver
from tui.visual_grid import VisualGrid
from tui.measures import Area, Segment, Len, LenT
from tui.placements import GPlace
from tui.text_box import TBox
from tui.controls import Btn, Clock, HPanel, DirP, BaseVisual


from tui.placements import PPlace, HPosEnum


###### GUI ELEMENTS ######
app_is_running = True
vg: VisualGrid = None 

log_panel = TBox(g_place=(1, 1, 1, 1))

col_defs = [(50, "*"), (50, "*")]

row_defs = [(1, "a"), 
            (50, "*"), 
            (50, "*")]

vg_children = [
    HPanel(None, 
           [Btn("edit"), Btn("view"), Btn("settings"), Btn("help"), 
            Btn("about"), Clock(p_place=PPlace(hPos=HPosEnum.RIGHT))])
    .g_at((0, 1, 0, 2)),
    
    DirP(".").g_at((1, 0)),
    log_panel.g_at((1, 1)),
    DirP(".").g_at((2, 0)),
    DirP(".").g_at((2, 1)),]


async def resolve_input_continous(stdscr, log_panel: TBox, vg: BaseVisual = None):
    global app_is_running
    
    while app_is_running:
        if log_panel is not None:
            resolve_input(stdscr, log_panel, vg)
        await asyncio.sleep(0.01)

def resolve_input(stdscr, log_panel, vg):
    global app_is_running
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
        


async def async_grid_refresh(grid: VisualGrid):
    while app_is_running:
        grid.draw()
        await asyncio.sleep(0.1)
        
    
async def run_async_tasks(stdscr):
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    stdscr.nodelay(True)  # Non-blocking mode
    global vg
    vg = VisualGrid(None, vg_children, row_defs=row_defs, col_defs=col_defs, stdscr=stdscr)
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

