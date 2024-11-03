import os
from pathlib import Path
from datetime import datetime
from typing import Callable, Any, List

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
            p_place: PPlace = PPlace()
    ):
        super().__init__(parent, [], Area(), g_place, p_place)
        self.title = title
        self.real_title = f"[{self.title}]"

    def draw(self):
        n_win = self.emit_window()
        n_win.addstr(0, 0, self.real_title)

    def get_width(self):
        return len(self.real_title)
    
    def get_dims(self):
        self.area.x1 = self.area.x0 + len(self.real_title)
        self.area.y1 = self.area.y0
        return self.area.get_dims()

class FileSystemBtn(Btn):
    def __init__(self, title, parent = None, g_place = None, p_place = PPlace()):
        
        super().__init__(title, parent, g_place, p_place)
        split = [s for s in title.split("/") if s != '']
        self.title = title
        self.real_title = self.title
        
class DirBtn(FileSystemBtn):
    def __init__(self, in_path: str, parent = None, g_place = None, p_place = PPlace()):
        super().__init__(in_path, parent, g_place, p_place)
    
    def click(self):
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
    def click(self):
        return super().click()

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
        
    def draw(self):
        self.real_title = self.title
        height, width = self.get_dims()
        table = self.emit_table(self.columns).draw_table()
                  
        items = 4 * [["abc", "def", "ghi", "jkl"]]
        cap = table.get_capacity()
        for idx, item in enumerate(items):
            if idx > cap - 1:
                break
            table.draw_row(idx, item)

class DirList(ListView):
    def __init__(self, title, parent=None, children=[], 
                 area=Area(), g_place=None, p_place=PPlace(), 
                 columns: list[Col]=[]):
        super().__init__(title, parent, children, area, g_place, p_place, None, columns)
        self.get_items_func = None
        self.columns = columns
        
    def draw(self):
        self.real_title = self.title
        height, width = self.get_dims()
        table = self.emit_table(self.columns).draw_table()
        dir_m = DirModel(abs_path=self.title)
        ok, fs_items = models.fs_model.get_tree(dir_m)
               
        cap = table.get_capacity()
        for idx, item in enumerate(fs_items):
            if idx > cap - 1:
                break
            row_data = []
            for col in self.columns:
                sub = getattr(item, col.title)
                row_data.append(sub)
            table.draw_row(idx, row_data)
            
            
            
