import os
from pathlib import Path
import time
from typing import Any
from tui.visual_grid import MainGrid
from tui.text_box import TBox
from tui.controls import Btn, Clock, HPanel, DirP, RadioPanel, ToggleButton, TableView
from tui.elementary.placements import PPlace, HPosEnum
from tui.n_window import Col
from tui.progress_bar import HProgressBar, VProgressBar
import models.fs_model
import csound_tweaking.examples.csound_py_test as examples
from utils.wrapped_job import WrappedJob
import tui.signal_resolver
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

my_dir_provider0 = models.fs_model.DirProvider()
my_dir_provider1 = models.fs_model.DirProvider()
my_dir_provider2 = models.fs_model.DirProvider()

curr_path = str(Path(".").resolve())
dir_list = TableView(curr_path, columns=dir_table_cols, 
                     get_items_func=lambda tv: my_dir_provider0.get_items(tv.title)
                         )

dir_list_2 = TableView(curr_path, columns=dir_table_cols, 
                     get_items_func=lambda tv: my_dir_provider1.get_items(tv.title)
                         )

dir_list_3 = TableView(curr_path, columns=dir_table_cols, 
                     get_items_func=lambda tv: my_dir_provider2.get_items(tv.title)
                         )

prog_bar = HProgressBar(None, get_val_func=lambda: prog_bar_value, max_val=100)

mix_panel = HPanel(children= [VProgressBar(None, get_val_func=lambda: prog_bar_value, max_val=100, p_place=PPlace(hPos=HPosEnum.LEFT)),
                              VProgressBar(None, get_val_func=lambda: prog_bar_value, max_val=100, p_place=PPlace(hPos=HPosEnum.LEFT)),
                              VProgressBar(None, get_val_func=lambda: prog_bar_value, max_val=100, p_place=PPlace(hPos=HPosEnum.LEFT))])


def start_csd(btn: Btn):
    ...

def stop_csd(btn: Btn):
    ...

def select_layout(_, a):
    vg.children = all_layouts[a]
    tui.signal_resolver.init_screen(None)
    
wrapped_job = WrappedJob(job_func=examples.run_example_2)
radio = ToggleButton(label="abc")
radio_panel = RadioPanel(label="layout:", choices=["a", "b", "c"], select_func=select_layout)
vg_children_quad = [
    HPanel(children=[Btn("edit"), Btn("view"), Btn("settings"), Btn("help"), 
            Btn("about"), 
            Btn("start csd", click_func=lambda btn: wrapped_job.try_run()), 
            Btn("stop csd", click_func=stop_csd), 
            radio_panel,
            Clock(p_place=PPlace(hPos=HPosEnum.RIGHT))])
    .g_at((0, 1, 0, 2)),
    
    DirP(".").g_at((1, 0)), dir_list.g_at((1, 4, 1, 1)),
    log_panel.g_at((2, 0)), 
    mix_panel.g_at((3, 1, 0, 1)),
    prog_bar.g_at((4, 1, 0, 1))
    ]


vg_children_quad_1 = [
    HPanel(children=[Btn("edit"), Btn("view"),
            radio_panel,
            Clock(p_place=PPlace(hPos=HPosEnum.RIGHT))])
    .g_at((0, 1, 0, 2)),
    dir_list_2.g_at((1, 4, 0, 1)),
    dir_list_3.g_at((1, 4, 1, 1)),
    ]

vg_children_quad_2 = [
    HPanel(children=[Btn("edit"), Btn("view"), Btn("settings"), Btn("help"), 
            Btn("about"), 
            Btn("start csd", click_func=lambda btn: wrapped_job.try_run()), 
            Btn("stop csd", click_func=stop_csd), 
            radio_panel,
            Clock(p_place=PPlace(hPos=HPosEnum.RIGHT))])
    .g_at((0, 1, 0, 2)),
    
    DirP(".").g_at((1, 0)), dir_list.g_at((1, 4, 1, 1)),
    log_panel.g_at((2, 0)), 
    mix_panel.g_at((3, 1, 0, 1)),
    prog_bar.g_at((4, 1, 0, 1))
    ]

all_layouts = [vg_children_quad, vg_children_quad_1, vg_children_quad_2]

vg = MainGrid(vg_children_quad, row_defs=row_defs, col_defs=col_defs)
vg.input_resolver.report_click_func =    \
    lambda obj, key, my, mx, mz, bs:     \
        log_panel.log(f"k:{key}, bs:{bs} ({my}, {mx}, {mz})")
        
        
def update_progress_bar():
    while True:
        global prog_bar_value
        prog_bar_value = ((prog_bar_value * 10 + 10) % 1000)/10
        time.sleep(0.05)        
        
non_ui_tasks = [update_progress_bar]
