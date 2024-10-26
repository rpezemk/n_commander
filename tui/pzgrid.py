from enum import Enum
from tui.measures import LenT, Len
from tui.controls import VisualHierarchy, HPosEnum
from tui.placements import GPlace, PanelPlacement
from tui.measures import Area, Segment
import tui.measures

class VisualGrid(VisualHierarchy):
    def __init__(self, parent, children: list[VisualHierarchy] = None, 
                 area: Area = Area(), 
                 grid_placement: GPlace = GPlace(0, 0, 0, 0), 
                 panel_placement: PanelPlacement = PanelPlacement(),
                 row_defs: list[Len] = [Len(100, LenT.STAR)],
                 col_defs: list[Len] = [Len(100, LenT.STAR)],
                 stdscr = None
                 ):
        super().__init__(parent, children, area, grid_placement, panel_placement)
        self.row_defs = row_defs
        self.col_defs = col_defs
        self.stdscr = stdscr
        
    def draw(self):
        self.area = Area(0, 0, *self.stdscr.getmaxyx())
        n_rows, n_cols = self.area.get_dims()
        v_lengths = tui.measures.get_effective_lengths(self.row_defs, n_rows)
        h_lengths = tui.measures.get_effective_lengths(self.col_defs, n_cols)
        
        for ch in self.children:
            row_no = ch.grid_placement.row_no
            row_sp = ch.grid_placement.row_span
            col_no = ch.grid_placement.col_no
            col_sp = ch.grid_placement.col_span
            
            v_sub = v_lengths[row_no:row_no+row_sp]
            h_sub = h_lengths[col_no:col_no+col_sp]
            
            v_seg = v_sub[0]
            h_seg = h_sub[0]
            v_sum = sum([h.diff() for h in v_sub])
            h_sum = sum([h.diff() for h in h_sub])
            ch.area = Area(v_seg.v0, h_seg.v0, v_seg.v0+v_sum, h_seg.v0+h_sum)
            ch.draw()
            