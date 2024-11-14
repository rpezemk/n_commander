import os
from pathlib import Path
from datetime import datetime
import threading
from typing import Callable, Any, List, Tuple

from tui.t_window import TableWindow
from utils import os_utils, string_utils
from tui.elementary.placements import GPlace, HPosEnum, PPlace
from tui.elementary.measures import Area, Col
from tui.base_visual import BaseVisual
from models.fs_model import DirModel, FileModel, FsItem, TreeProvider
import models.fs_model

fs_prov = TreeProvider(os_utils.get_nice_dir_content)

class Btn(BaseVisual):
    def __init__(
        self, title: str, parent: BaseVisual = None,
            g_place: GPlace = None, 
            p_place: PPlace = PPlace(),
            click_func: Callable[['Btn'], None] = None
    ):
        super().__init__(parent, [], Area(), g_place, p_place)
        self.title = title
        self.real_title = f"[{self.title}]"
        self.click_func = click_func

    def draw(self):
        n_win = self.emit_window()
        n_win.addstr(0, 0, self.real_title)

    def get_width(self):
        return len(self.real_title)
    
    def get_dims(self):
        self.area.x1 = self.area.x0 + len(self.real_title)
        self.area.y1 = self.area.y0
        return self.area.get_dims()

    def simple_click(self, my, mx, bs):
        # super().simple_click(my, mx, bs)
        if self.click_func is None:
            return
        t1 = threading.Thread(target=self.click_func, args=[self])
        t1.start() 
        #self.click_func(self)
        ...
     
class RadioChoice(BaseVisual):
    def __init__(self, parent = None, g_place = None, p_place = PPlace(), label = "<>"):
        super().__init__(parent, None, Area(), g_place, p_place)
        self.label = label
        
    def get_width(self):
        return len(self.label) + 4
    
    def get_dims(self):
        self.area.x1 = self.area.x0 + len(self.label) + 6
        self.area.y1 = self.area.y0
        return self.area.get_dims()
    
    def draw(self):
        n_win = self.emit_window()
        n_win.addstr(0, 0, "[ ]" + self.label)
        
    def simple_click(self, my, mx, bs):
        # super().simple_click(my, mx, bs)
        ...

class RadioPanel(BaseVisual):
    def __init__(self, children = None, g_place = None, 
                 select_func: Callable[[int],None] = None, 
                 choices: list[str] = []):
        super().__init__(None, children, Area(), g_place, PPlace())
        self.choices = choices
        for choice in self.choices:
            self.children.append(RadioChoice(label=choice))
        
    def get_width(self):
        return 4
    
    def get_dims(self):
        self.area.x1 = self.area.x0 + 4
        self.area.y1 = self.area.y0
        return self.area.get_dims()
    
    def draw(self):
        x0 = self.area.x0
        y0 = self.area.y0
        curr_x_left = 1
        curr_x_right = self.area.x1 + 1
        last_width = 0
        widths = [0]
        for item in self.children:
            item.area.x0 = curr_x_left + x0
            item.area.x1 = item.area.x0 + item.get_width()
            last_width = item.get_width()
            widths.append(last_width)
            curr_x_left += last_width + 1
            item.area.y0 = self.area.y0
            item.area.y1 = self.area.y1
            item.draw() 
            
        res_width = sum(widths) + len(widths) - 2
        self.area.x1 = self.area.x0 + res_width
        h, w = self.area.get_dims()
        n_win = self.emit_window()
        n_win.addstr(0, 0, "[")
        n_win.addstr(0, w-1, "]")
        
    def simple_click(self, my, mx, bs):
        # super().simple_click(my, mx, bs)
        ...
        
class FileSystemBtn(Btn):
    def __init__(self, title, parent = None, g_place = None, p_place = PPlace()):
        
        super().__init__(title, parent, g_place, p_place)
        split = [s for s in title.split("/") if s != '']
        self.title = title
        self.real_title = self.title
        
class DirBtn(FileSystemBtn):
    def __init__(self, in_path: str, parent = None, g_place = None, p_place = PPlace()):
        super().__init__(in_path, parent, g_place, p_place)
    
    def simple_click(self, my, mx, bs):
        if self.parent is not None:
            if self.title != "../":
                p = os.path.join(self.parent.title, self.title)
            else:
                p = str(Path(self.parent.title).parent)
            self.parent.title = p
        # return super().click()

class FileBtn(FileSystemBtn):
    def __init__(self, title, parent = None, g_place = None, p_place = PPlace()):
        super().__init__(title, parent, g_place, p_place)
    def simple_click(self, my, mx, bs):
        return super().simple_click(my, mx, bs)

class Clock(Btn):
    def __init__(self, parent=None,
                g_place: GPlace = None, 
                p_place: PPlace = PPlace()):
        self.title = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.real_title = f"[{self.title}]"
        super().__init__(self.title, parent, g_place, p_place)

    def draw(self):
        self.title = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.real_title = f"[{self.title}]"
        super().draw()
        
    def get_width(self):
        return len(self.real_title)

class HPanel(BaseVisual):
    def __init__(self, parent=None, children=[],
            g_place: GPlace = None, 
            p_place: PPlace = PPlace()):
        super().__init__(parent, children, p_place=p_place, g_place=g_place)

    def draw(self):
        curr_x_left = 1
        h, w = self.area.get_dims()
        curr_x_right = self.area.x1 + 1
        for item in self.children:
            if item.p_place.hPos == HPosEnum.LEFT:
                item.area.x0 = curr_x_left
                item.area.x1 = item.area.x0 + item.get_width()
                curr_x_left += item.get_width() + 1
            if item.p_place.hPos == HPosEnum.RIGHT:
                curr_x_right -= item.get_width()
                item.area.x0 = curr_x_right
            
            item.area.y0 = self.area.y0
            item.area.y1 = self.area.y1
            
            item.draw()


class Panel(BaseVisual):
    def __init__(
        self,
        title: str,
        parent=None,
        children: list[BaseVisual] = [],
        area: Area = Area(),
        g_place: GPlace = None, 
        p_place: PPlace = PPlace()
    ):
        super().__init__(parent, children, area, g_place=g_place, p_place=p_place)
        self.title = title

    def draw(self):
        ...

class ItemPanel(Panel):
    def __init__(self, title, parent=None, children = [], area = Area(), 
                 g_place = None, p_place = PPlace(), 
                 get_items_func:Callable[[],list[Btn]]=None,
                 get_item_width_func:Callable[[],int]=None):
        super().__init__(title, parent, children, area, g_place, p_place)
        self.get_items_func = get_items_func
        
    def draw(self) -> None:
        self.real_title = self.title
        height, width = self.get_dims()
        win = self.emit_window().draw_table()
        win.addstr(0, 1, self.title)
        if self.get_items_func is None:
            return
        
        if height - 3 < 0:
            return
        
        self.children = self.get_items_func()
        
        y0 = 1 + self.area.y0 
        x0 = self.area.x0 + 2
        children_to_draw = []
        
        ch_groups: list[DirBtn | FileBtn] = string_utils.group_elements_by_n(self.children, height - 2)
        
        n_groups = len(ch_groups)
        for idx, ch_group in enumerate(ch_groups):
            gr_width = max([len(ch.real_title) for ch in ch_group]) + 1  
            if x0 + gr_width > width:
                break
            
            for idx, ch in enumerate(ch_group):    
                y_offset = y0 + (idx % (height - 2))
                ch.area = Area(y_offset, x0, y_offset, x0 + len(ch.real_title))
                ch.parent = self
                children_to_draw.append(ch)
            
            x0 += gr_width

        for ch in children_to_draw:
            ch.draw()


            
class DirP(ItemPanel):
    def __init__(self, title = None,
                    g_plc: GPlace = None, 
                    p_place: PPlace = PPlace()
                    ):
        absolute_path = title
        if absolute_path is None or title == '' or title == '.':
            absolute_path = str(Path(".").resolve())
        split = [s for s in title.split("/") if s != '']
        self.title = str(Path(split[-1]).resolve())
        self.real_title = self.title
        super().__init__(absolute_path, g_place=g_plc, p_place=p_place, get_items_func=self.get_items)

    def get_items(self):
        absolute_path = self.title
        if absolute_path is None or self.title == '' or self.title == '.':
            absolute_path = str(Path(".").resolve())
            
        dirOk, dirs, files, errStr = os_utils.try_get_dir_content(absolute_path)
        
        return [*list([DirBtn(dir) for dir in dirs]), *list([FileBtn(file) for file in files])]
    
   
   
        
class ListView(Panel):
    def __init__(self, title, parent=None, children = [], 
                 area = Area(), g_place = None, p_place = PPlace(), 
                 get_items_func: Callable[[None],list[Any]]=None, columns=list[str]):
        super().__init__(title, parent, children, area, g_place, p_place)
        self.get_items_func = get_items_func
        self.columns = columns
        self.items_by_row_no = []
        
    def draw(self):
        ...

class TableView(ListView):
    def __init__(self, title, parent=None, children=[], 
                 area=Area(), g_place=None, p_place=PPlace(), 
                 columns: list[Col]=[], 
                 get_items_func:Callable[['TableView'], Tuple[bool,list[Any]]] = None,
                 click_func:Callable[['TableView', int, int], None] = None,):
        super().__init__(title, parent, children, area, g_place, p_place, None, columns)
        self.get_items_func = get_items_func
        self.columns = columns
        self.click_func = click_func
        self.data_by_row_no = []
        self.table: TableWindow = None
        self.needs_redraw = True
        self.orig_data = []
        self.idx_offset = 0
        
    def draw(self):
        # if not self.needs_redraw:
        #     return
        self.real_title = self.title
        self.table = self.emit_table(self.columns).draw_table(self.real_title)
        dir_m = DirModel(abs_path=self.title)
        ok, fs_items = self.get_items_func(self)
        self.orig_data = fs_items
        cap = self.table.get_capacity()
        self.data_by_row_no = []
        self.real_items_by_row_no = []
        n_items = len(fs_items)
        n_overflow_items = n_items - cap
        max_idx_offset = max(0, n_overflow_items)
        real_idx_offset =  min(self.idx_offset, max_idx_offset)
        
        if n_overflow_items < 1:
            shown_items = fs_items
        else:
            shown_items = fs_items[real_idx_offset:][:cap]
            
        for idx, item in enumerate(shown_items):
            if idx > cap - 1:
                break
            self.real_items_by_row_no.append((idx, item))
            vis_row_data = []
            row_data = []
            for col in [col1 for col1 in self.columns]:
                sub = getattr(item, col.title, "")
                row_data.append(sub)
                if col.is_hidden == False:
                    vis_row_data.append(sub)
            self.data_by_row_no.append((idx, row_data))
            self.table.draw_row(idx, vis_row_data)
        self.needs_redraw = False
        
    def simple_click(self, my, mx, bs):
        # self.click_func(self, my, mx)
        local_x = mx - self.area.x0
        if self.table is None:
            return
        
        
        y0 = self.area.y0
        y1 = self.area.y1
        x1 = self.area.x1
        cap = self.table.get_capacity()
        
        if mx == x1 and my == y0 and self.idx_offset -1 >= 0:
            self.idx_offset -= 1
            return
        
        n_items = len(self.orig_data)
        n_overflow_items = n_items - cap
        max_idx_offset = max(0, n_overflow_items)
        
        if mx == x1 and my == y1 and self.idx_offset + 1 <= max_idx_offset:
            self.idx_offset += 1
            return 
        
        y_min = y0 + 2
        row_no = my - y_min
        if len(self.data_by_row_no) < row_no + 1:
            return
        sel_seg = [seg for seg in self.table.segments if seg.v0 <= local_x <= seg.v1]
        if len(sel_seg) == 0:
            return
        seg = sel_seg[0]
        vis_idx = self.table.segments.index(seg)
        visible_columns = [col for col in self.columns if col.is_hidden == False]
        if len(visible_columns) < vis_idx + 1:
            return
        col = visible_columns[vis_idx]
        if col.click_func is None:
            return
        
        data = self.data_by_row_no[row_no][1]
        real_item = self.real_items_by_row_no[row_no]
        col.click_func(self, data, real_item)

        pass
    
    
    def wheel_up(self, my, mx, bs):
        y0 = self.area.y0
        y1 = self.area.y1
        x1 = self.area.x1
        
        if self.idx_offset -1 >= 0:
            self.idx_offset -= 1

    
        
    def wheel_down(self, my, mx, bs):
        cap = self.table.get_capacity()
        n_items = len(self.orig_data)
        n_overflow_items = n_items - cap
        max_idx_offset = max(0, n_overflow_items)
        
        if self.idx_offset + 1 <= max_idx_offset:
            self.idx_offset += 1
            return 