import curses
import sys
import asyncio

from tui import signal_resolver
from tui.visual_grid import VisualGrid
from tui.text_box import TBox
from tui.controls import Btn, Clock, HPanel, DirP, ListView
from tui.placements import PPlace, HPosEnum
import tui.n_window
from tui.n_window import ColInfo
from tui.input_resolver import InputResolver

###### GUI ELEMENTS ######
app_is_running = True
vg: VisualGrid = None 

log_panel = TBox(g_place=(1, 1, 1, 1))

col_defs = [(50, "*"), (50, "*")]

row_defs = [(1, "a"), 
            (50, "*"), 
            (50, "*")]

dir_table_cols = [ColInfo("a", (10, "*")), ColInfo("a", (10, "*")), ColInfo("b", (10, "*")), ColInfo("c", (10, "*"))]

vg_children_quad = [
    HPanel(children=[Btn("edit"), Btn("view"), Btn("settings"), Btn("help"), 
            Btn("about"), Clock(p_place=PPlace(hPos=HPosEnum.RIGHT))])
    .g_at((0, 1, 0, 2)),
    
    DirP(".").g_at((1, 0)), log_panel.g_at((1, 1)),
    DirP(".").g_at((2, 0)), ListView(".", columns=dir_table_cols).g_at((2, 1)),
    ]

vg_children_split_h = [
    HPanel(children=[Btn("edit"), Btn("view"), Btn("settings"), Btn("help"), 
                     Btn("about"), Clock(p_place=PPlace(hPos=HPosEnum.RIGHT))])
    .g_at((0, 1, 0, 2)),
    
    DirP(".").g_at((1, 1, 0, 2)),
    ListView(".", columns=dir_table_cols).g_at((2, 1, 0, 2)),
    ]

def soft_close_app():
    global app_is_running
    app_is_running = False

input_resolver = InputResolver(None, 
                               get_scr_func=(lambda: signal_resolver.stdscr), 
                               root_obj_func=lambda: vg.get_all_objects(), 
                               turn_off_func=soft_close_app,
                               report_click_func=
                                   lambda key, id, mx, my, mz, bs: 
                                       log_panel.log(f"M: k:{key}, bs:{bs} ({my}, {mx}, {mz})"))



async def async_grid_refresh(grid: VisualGrid):
    while app_is_running:
        grid.draw()
        tui.n_window.render_frame()
        await asyncio.sleep(0.1)
        
    
async def run_async_tasks(stdscr):
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    stdscr.nodelay(True)  # Non-blocking mode
    global vg
    vg = VisualGrid(None, vg_children_quad, row_defs=row_defs, col_defs=col_defs, stdscr=stdscr)
    input_task = asyncio.create_task(input_resolver.start())
    tui_task = asyncio.create_task(async_grid_refresh(vg))
    await tui_task
    stdscr.clear()
    stdscr.refresh()
    
def main(stdscr):
    curses.curs_set(0)
    signal_resolver.init_screen(stdscr)
    asyncio.run(run_async_tasks(stdscr))

if __name__ == "__main__":
    curses.wrapper(main)
    # try:
    #     #curses.wrapper(main)
    # except Exception as e:
    #     print(f"Error: {e}")

