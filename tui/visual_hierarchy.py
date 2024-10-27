from tui.measures import Area
from tui.placements import GPlace, PPlace

class VisualHierarchy:
    def __init__(
        self,
        parent: "VisualHierarchy",
        children: list["VisualHierarchy"] = None,
        
        area : Area = Area(),
        grid_placement: GPlace = None, 
        panel_placement: PPlace = PPlace()
    ):
        self.parent = parent
        self.children = [] if children is None else children
        self.area = area
        self.grid_placement = grid_placement
        self.panel_placement = panel_placement
        
        for child in [ch for ch in self.children if ch is not None]:
            child.parent = self
        
    def append_child(self, child: "VisualHierarchy"):
        self.children.append(child)
        child.parent = self

    def get_all_objects(self) -> list['VisualHierarchy']:
        res = [self] 
        for ch in self.children:
            ch_objs = ch.get_all_objects()
            for ch_ob in ch_objs:
                res.append(ch_ob)
        
        return res
    
    def draw(self):
        ...
        
    def check_point_belongs(self, x: int, y: int):
        check_h = self.area.x0 <= x <= self.area.x1
        check_v = self.area.y0 <= y <= self.area.y1
        return check_h and check_v