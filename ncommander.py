import curses
import os
from pathlib import Path
import sys
import asyncio

from tui import signal_resolver
from tui.visual_grid import MainGrid
from tui.text_box import TBox
from tui.controls import Btn, Clock, HPanel, DirP, ListView, TableView
from tui.elementary.placements import PPlace, HPosEnum
import tui.n_window
from tui.n_window import Col
from tui.input_resolver import InputResolver
from tui.progress_bar import HProgressBar, VProgressBar
import models.fs_model
from utils import os_utils

prog_bar_value = 0

app_is_running = True
vg: MainGrid = None 

log_panel = TBox(g_place=(1, 1, 1, 1))

col_defs = [(50, "*"), (50, "*")]

row_defs = [(1, "a"), 
            (50, "*"), 
            (50, "*"), 
            (50, "*"), 
            (1, "a")]

dir_table_cols = [Col("abs_path", (15, "*", "h")) ,Col("rel_path", (10, "*")), Col("ext", (5, "a"))]

curr_path = str(Path(".").resolve())

def click_tv_method(tv: TableView, my: int, mx: int):
    y0 = tv.area.y0
    y1 = tv.area.y1
    
    y_min = y0 + 2
    y_max = y1 - 1
    row_no = my - y_min
    
    if y_min <= my <= y_max and 0 <= row_no <= len(tv.items_by_row_no) - 1:
        
        child_abs_path = tv.items_by_row_no[row_no][1][0]
        if os.path.isdir(child_abs_path):
            tv.title = child_abs_path


dir_list = TableView(curr_path, columns=dir_table_cols, 
                     get_items_func=lambda dir_list: 
                         models.fs_model.get_tree(
                             models.fs_model.DirModel(abs_path=dir_list.title)
                             ),
                     click_func=click_tv_method
                         )

prog_bar = HProgressBar(None, get_val_func=lambda: prog_bar_value, max_val=100)

mix_panel = HPanel(children= [VProgressBar(None, get_val_func=lambda: prog_bar_value, max_val=100, p_place=PPlace(hPos=HPosEnum.LEFT)),
                              VProgressBar(None, get_val_func=lambda: prog_bar_value, max_val=100, p_place=PPlace(hPos=HPosEnum.LEFT)),
                              VProgressBar(None, get_val_func=lambda: prog_bar_value, max_val=100, p_place=PPlace(hPos=HPosEnum.LEFT))])


vg_children_quad = [
    HPanel(children=[Btn("edit"), Btn("view"), Btn("settings"), Btn("help"), 
            Btn("about"), Clock(p_place=PPlace(hPos=HPosEnum.RIGHT))])
    .g_at((0, 1, 0, 2)),
    
    DirP(".").g_at((1, 0)), dir_list.g_at((1, 4, 1, 1)),
    log_panel.g_at((2, 0)), 
    mix_panel.g_at((3, 1, 0, 1)),
    prog_bar.g_at((4, 1, 0, 1))
    ]




async def update_progress_bar():
    global prog_bar_value
    while True:
        prog_bar_value = ((prog_bar_value * 10 + 1) % 1000)/10
        await asyncio.sleep(0.01)
        
async def start_update_progress_bar():
        asyncio.create_task(update_progress_bar())

def main(stdscr):
    curses.curs_set(0)
    signal_resolver.init_screen(stdscr)
    vg = MainGrid(vg_children_quad, row_defs=row_defs, col_defs=col_defs, stdscr=stdscr)
    vg.input_resolver.report_click_func =    \
        lambda obj, key, my, mx, mz, bs:     \
            log_panel.log(f"k:{key}, bs:{bs} ({my}, {mx}, {mz})")
            # (self, id, mx, my, mz, bs)
    asyncio.run(vg.run_async_tasks(stdscr, [start_update_progress_bar]))

if __name__ == "__main__":
    curses.wrapper(main);
    # try:
    #     #curses.wrapper(main)
    # except Exception as e:
    #     print(f"Error: {e}")

