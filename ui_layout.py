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
from models.fs_model import DirProvider
import csound_tweaking.examples.csound_py_test as examples
from utils.wrapped_job import WrappedJob
import tui.signal_resolver

############# global variables ##############
prog_bar_value = 0
app_is_running = True
main_vg: MainGrid = None 


############# mvc methods #############
def get_prog_bar_value():
    global prog_bar_value
    return prog_bar_value


def click_sel(tv: TableView, real_idx_item_tup: Any):
    if real_idx_item_tup is None or len(real_idx_item_tup) < 2:
        return
    real_item = real_idx_item_tup[1]
    
    if isinstance(real_item, models.fs_model.ParentDirModel):
        return
    real_item.sel = not real_item.sel


def click_rel_path(tv: TableView, data: list[str]):
    child_abs_path = data[1]
    if os.path.isdir(child_abs_path.abs_path):
        tv.title = child_abs_path.abs_path
        tv.idx_offset = 0

    
def bool_to_bracket(sel):
    return "[x]" if sel is True else "[ ]"


def select_layout(_, a):
    main_vg.children = all_layouts[a]
    tui.signal_resolver.init_screen(None)
    
def update_progress_bar():
    while True:
        global prog_bar_value
        prog_bar_value = ((prog_bar_value * 10 + 10) % 1000)/10
        time.sleep(0.05)  


############################# TUI DEFINITIONS ############################### 
log_panel = TBox()

col_defs = [(50, "*"), (50, "*")]

row_defs = [(1, "a"), 
            (50, "*"), 
            (50, "*"), 
            (50, "*"), 
            (1, "a")]


dir_table_cols = [
    Col("sel", (3, "a"), show_func=bool_to_bracket, click_func=click_sel),
    Col("abs_path", (15, "*", "h")),
    Col("rel_path", (10, "*"), click_func=click_rel_path), 
    Col("size", (10, "a")), 
    Col("ext", (5, "a"))
    ]

dot = str(Path(".").resolve())

dir_list = TableView(dot, columns=dir_table_cols, provider_type=DirProvider)
dir_list_2 = TableView(dot, columns=dir_table_cols, provider_type=DirProvider)
dir_list_3 = TableView(dot, columns=dir_table_cols, provider_type=DirProvider)

prog_bar = HProgressBar(None, get_val_func=lambda: prog_bar_value, max_val=100)

mix_panel = HPanel(children= [VProgressBar(get_val_func=get_prog_bar_value, max_val=100),
                              VProgressBar(get_val_func=get_prog_bar_value, max_val=100),
                              VProgressBar(get_val_func=get_prog_bar_value, max_val=100)])
    
wrapped_job = WrappedJob(job_func=examples.run_example_2)

radio_panel = RadioPanel(label="layout:", choices=["a", "b", "c"], select_func=select_layout)

menu_panel = HPanel(children=[radio_panel, Btn("edit"), Btn("view"), Btn("settings"), Btn("help"), 
            Btn("about"), 
            Btn("start csd", click_func=lambda btn: wrapped_job.try_run()), 
            Clock(p_place=PPlace(hPos=HPosEnum.RIGHT))]).g_at((0, 1, 0, 2))

vg_children_quad = [
    menu_panel,
    DirP(".").g_at((1, 0)), dir_list.g_at((1, 4, 1, 1)),
    log_panel.g_at((2, 0)), 
    mix_panel.g_at((3, 1, 0, 1)),
    prog_bar.g_at((4, 1, 0, 1))
    ]


vg_children_quad_1 = [
    menu_panel,    
    dir_list_2.g_at((1, 4, 0, 1)),
    dir_list_3.g_at((1, 4, 1, 1)),
    ]

vg_children_quad_2 = [
    menu_panel,
    DirP(".").g_at((1, 0)), dir_list.g_at((1, 4, 1, 1)),
    log_panel.g_at((2, 0)), 
    mix_panel.g_at((3, 1, 0, 1)),
    prog_bar.g_at((4, 1, 0, 1))
    ]

all_layouts = [vg_children_quad, vg_children_quad_1, vg_children_quad_2]


################## MAIN OBJECT ###################
main_vg = MainGrid(vg_children_quad, row_defs=row_defs, col_defs=col_defs)
main_vg.input_resolver.report_click_func =    \
    lambda obj, key, my, mx, mz, bs:     \
        log_panel.log(f"k:{key}, bs:{bs} ({my}, {mx}, {mz})")
        

################ TASKS #################                
non_ui_tasks = [update_progress_bar]
