from enum import Enum
from tui.measures import LenT, Len
from tui.controls import BaseVisual, HPosEnum
from tui.placements import GPlace, PPlace
from tui.measures import Area, Segment
import tui.measures

class VisualGrid(BaseVisual):
    def __init__(self, parent, children: list[BaseVisual] = None, 
                 area: Area = Area(), 
                 g_place: GPlace = GPlace(0, 0, 0, 0), 
                 panel_placement: PPlace = PPlace(),
                 row_defs: list[Len] = [Len(100, LenT.STAR)],
                 col_defs: list[Len] = [Len(100, LenT.STAR)],
                 stdscr = None
                 ):
        # row_defs = [(1, "a"), (50, "*"), (50, "*")]
        res_row_defs = []
        
        super().__init__(parent, children, area, g_place, panel_placement)
        self.row_defs = row_defs
        self.col_defs = col_defs
        self.stdscr = stdscr
        
    def draw(self):
        self.area = Area(0, 0, *self.stdscr.getmaxyx())
        h, w = self.get_dims()
        v_lengths = tui.measures.get_effective_lengths(self.row_defs, h - 1)
        h_lengths = tui.measures.get_effective_lengths(self.col_defs, w - 1)
        
        for ch in self.children:
            if ch == None:
                continue
            
            row_no = ch.g_place.row_no
            row_sp = ch.g_place.row_span
            col_no = ch.g_place.col_no
            col_sp = ch.g_place.col_span
            
            v_sub = v_lengths[row_no:row_no+row_sp]
            h_sub = h_lengths[col_no:col_no+col_sp]
            
            v_seg = v_sub[0]
            h_seg = h_sub[0]
            v_sum = sum([h.diff() for h in v_sub]) - 1
            h_sum = sum([h.diff() for h in h_sub]) - 1
            ch.area = Area(v_seg.v0, h_seg.v0, v_seg.v0+v_sum, h_seg.v0+h_sum)
            ch.draw()