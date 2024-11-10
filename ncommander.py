import curses
import os
from pathlib import Path
import sys
import asyncio
from typing import Any

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


def click_sel(tv: TableView, data: list[str], real_idx_item_tup: Any):
    if real_idx_item_tup is None or len(real_idx_item_tup) < 2:
        return
    real_item = real_idx_item_tup[1]
    
    if isinstance(real_item, models.fs_model.ParentDirModel):
        return
    
    real_item.sel = not real_item.sel
    pass

def click_rel_path(tv: TableView, data: list[str], real_item: Any):
    child_abs_path = data[1]
    if os.path.isdir(child_abs_path):
        tv.title = child_abs_path
        tv.idx_offset = 0
    pass
    ...
    
def bool_to_bracket(sel):
    return "[x]" if sel is True else "[ ]"

dir_table_cols = [
    Col("sel", (3, "a"), show_func=bool_to_bracket, click_func=click_sel),
    Col("abs_path", (15, "*", "h")),
    Col("rel_path", (10, "*"), click_func=click_rel_path), 
    Col("size", (10, "a")), 
    Col("ext", (5, "a"))
    ]

my_dir_provider = models.fs_model.DirProvider()




curr_path = str(Path(".").resolve())
dir_list = TableView(curr_path, columns=dir_table_cols, 
                     get_items_func=lambda tv: my_dir_provider.get_items(tv.title)
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
    #     curses.wrapper(main)
    # except Exception as e:
    #     print(f"Error: {e}")

