from typing import Any
import tui
import tui.elementary
from tui.elementary.measures import Area, Col, Segment
from tui.n_window import TS, NWindow
import tui.n_window

class TableWindow(NWindow):
    def __init__(self, h, w, y0, x0, title="", columns:list[Col]=[]):
        super().__init__(h, w, y0, x0, title)    
        self.columns = columns
        self.rows = []
        self.segments = []
            
    def draw_table(self, title):
        h, w = self.area.get_dims()
        n_cols = len(self.columns)
        
        inner_width = w - (n_cols - 1) - 2
        filled_width = w - inner_width
        col_widths = list([col.width for col in self.columns])
        segments = tui.elementary.measures.get_segments(col_widths, inner_width, self.columns)
        self.segments = segments
        self.spacers = [Segment(seg.v0+idx, seg.v1+idx) for idx, seg in enumerate(segments)]
        
        test_blank_sum = sum([w.v1 - w.v0 for w in segments])
        
        res_title = title
        
        top_line = (TS.s.top_left + " " + res_title + " ").ljust(w-1, TS.s.dash_h) + TS.s.top_right
        
        sec_line = TS.s.left_conn \
                   + TS.s.upper_conn.join([(self.columns[idx].title).ljust(seg.v1 - seg.v0, TS.s.horizontal) for idx, seg in enumerate(segments)]) \
                   + TS.s.right_conn
                   
        mid_line = TS.s.vertical \
            + TS.s.vertical.join([" " * (seg.v1 - seg.v0) for idx, seg in enumerate(segments)]) \
            + TS.s.vertical
        btm_line = TS.s.bottom_left + TS.s.lower_conn.join([TS.s.horizontal * (seg.v1 - seg.v0) for seg in segments]) + TS.s.bottom_right
        
        top_len = len(top_line)
        lines = [top_line,
                 sec_line,
                *( (h-3) * [mid_line]), 
                btm_line]
        tui.n_window.frame.draw_area(area=self.area, sub_lines=lines)
        return self
    
    def get_capacity(self) -> int:
        h, w = self.area.get_dims()
        return max(h - 3, 0)
        
    def draw_object_row(self, row_no=0, obj:Any = None):
        n_filled_cols = min(len(self.columns), len(obj))
        x0 = self.area.x0 + 1
        y0 = self.area.y0 + 2
        h, w = self.area.get_dims()
        if row_no > h - 4:
            return 
        for i in range(0, n_filled_cols):
            seg = self.spacers[i]
            x_offset = x0 + seg.v0
            y_offset = y0 + row_no
            data = obj[i]
            tui.n_window.frame.draw_area(area=Area(y_offset, x_offset, y_offset, x_offset + len(data)), sub_lines=[data])
                
    def draw_row(self, row_no=0, row_data:list[str] = []):
        n_filled_cols = min(len(self.columns), len(row_data))
        x0 = self.area.x0 + 1
        y0 = self.area.y0 + 2
        h, w = self.area.get_dims()
        if row_no > h - 4:
            return 
        for i in range(0, n_filled_cols):
            seg = self.spacers[i]
            x_offset = x0 + seg.v0
            y_offset = y0 + row_no
            data = row_data[i]
            max_len = min(seg.v1 - seg.v0, len(data))
            sdf = data[:max_len]
            tui.n_window.frame.draw_area(area=Area(y_offset, x_offset, y_offset, x_offset + max_len), sub_lines=[sdf])
        
