import curses
import sys
import asyncio

from tui import signal_resolver
from tui.visual_grid import MainGrid
from tui.text_box import TBox
from tui.controls import Btn, Clock, HPanel, DirP, ListView
from tui.placements import PPlace, HPosEnum
import tui.n_window
from tui.n_window import ColInfo
from tui.input_resolver import InputResolver

app_is_running = True
vg: MainGrid = None 

log_panel = TBox(g_place=(1, 1, 1, 1))

col_defs = [(50, "*"), (50, "*")]

row_defs = [(1, "a"), 
            (50, "*"), 
            (50, "*")]

dir_table_cols = [ColInfo("a", (10, "*")), ColInfo("a", (10, "*")), 
                  ColInfo("b", (10, "*")), ColInfo("c", (10, "*"))]

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


def main(stdscr):
    curses.curs_set(0)
    signal_resolver.init_screen(stdscr)
    vg = MainGrid(vg_children_quad, row_defs=row_defs, col_defs=col_defs, stdscr=stdscr)
    vg.input_resolver.report_click_func =    \
        lambda obj, key, bs, my, mx, mz:     \
            log_panel.log(f"k:{key}, bs:{bs} ({my}, {mx}, {mz})")
            
    asyncio.run(vg.run_async_tasks(stdscr))

if __name__ == "__main__":
    curses.wrapper(main)
    # try:
    #     #curses.wrapper(main)
    # except Exception as e:
    #     print(f"Error: {e}")

