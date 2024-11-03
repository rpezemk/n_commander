from tui.elementary.measures import Area
from tui.elementary.placements import GPlace, PPlace
import curses
from tui.n_window import NWindow
from tui.t_window import TableWindow
class BaseVisual:
    def __init__(
        self,
        parent: "BaseVisual",
        children: list["BaseVisual"] = None,
        area : Area = Area(),
        g_place: GPlace = None, 
        p_place: PPlace = PPlace()
    ):
        self.parent = parent
        self.children = [] if children is None else children
        self.area = area
        
        self.g_at(g_place)
        self.p_place = p_place
        
        for child in [ch for ch in self.children if ch is not None]:
            child.parent = self
        
    def append_child(self, child: "BaseVisual"):
        self.children.append(child)
        child.parent = self

    def get_all_objects(self) -> list['BaseVisual']:
        res = [self] 
        for ch in self.children:
            if ch is None:
                continue
            
            ch_objs = ch.get_all_objects()
            for ch_ob in ch_objs:
                res.append(ch_ob)
        
        return res
    
    def click(self):
        ...
    
    def draw(self):
        ...
        
    def check_point_belongs(self, x: int, y: int):
        check_h = self.area.x0 <= x <= self.area.x1
        check_v = self.area.y0 <= y <= self.area.y1
        return check_h and check_v
    
    def get_name(self):
        name = "abc"
        return name
    
    def g_at(self, g_place):
        temp_g_place = None
        match g_place:
            case _ if isinstance(g_place, GPlace):
                pass
            case (x,y):
                temp_g_place = GPlace(g_place[0], 1, g_place[1], 1)
            case (k, l, m, n):
                    temp_g_place = GPlace(*g_place)
            case _:
                temp_g_place = GPlace(1, 0, 1, 0)
        self.g_place = temp_g_place
        return self
        
    def emit_table(self, cols):
        h, w = self.get_dims()        
        n_table = TableWindow(h, w, self.area.y0, self.area.x0, columns=cols)
        return n_table
    
    
    def emit_window(self):
        h, w = self.get_dims()        
        n_win = NWindow(h, w, self.area.y0, self.area.x0)
        return n_win
    
    def get_dims(self):
        h, w = self.area.get_dims()        
        return h, w