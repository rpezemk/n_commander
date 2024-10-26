from enum import Enum
from tui.measures import LengthType, Length
from tui.controls import VisualHierarchy, HPosEnum
from tui.placements import GridPlacement, PanelPlacement
from tui.measures import Area, Segment
import tui.measures

class VisualGrid(VisualHierarchy):
    def __init__(self, parent, children: list[VisualHierarchy] = None, 
                 Area: Area = Area(), 
                 grid_placement: GridPlacement = GridPlacement(), 
                 panel_placement: PanelPlacement = PanelPlacement,
                 row_defs: list[Length] = [Length(100, LengthType.STAR)],
                 col_defs: list[Length] = [Length(100, LengthType.STAR)]
                 ):
        super().__init__(parent, children, Area(), grid_placement, panel_placement)
        self.row_defs = row_defs
        self.col_defs = col_defs
        
    def draw(self):
        height, width = self.area.get_dims()
        v_lengths = tui.measures.get_effective_lengths(self.row_defs, height)
        h_lengths = tui.measures.get_effective_lengths(self.col_defs, width)
        
        for ch in self.children:
            row_no = ch.grid_placement.row_no
            col_no = ch.grid_placement.col_no
            h_seg:Segment = h_lengths[:col_no][-1]
            v_seg:Segment = v_lengths[:row_no][-1]
            ch.area = Area(v_seg.v0, v_seg.v1, h_seg.v0, h_seg.v1)
            ch.draw()
            