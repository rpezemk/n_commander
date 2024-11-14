from enum import Enum
from typing import Any, Callable, Tuple

class Segment():
    def __init__(self, v0 = 0, v1 = 0, is_abs = False, is_hidden = False):
        self.v0 = v0
        self.v1 = v1
        self.is_abs = is_abs
        self.is_hidden = is_hidden
        
    def diff(self) -> int:
        return self.v1 - self.v0


class Area():
    def __init__(self, y0 = 0, x0 = 0, y1 = 0, x1 = 0):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1

    def get_dims(self) -> Tuple[int, int]:
        return self.y1 - self.y0 + 1, self.x1 - self.x0 + 1
    
    
class LenT(Enum):
    ABS = 1
    STAR = 2


class Length():
    def __init__(self, value: int, len_type: LenT = LenT.STAR, is_hidden=False):
        self.value = value
        self.len_type = len_type
        self.effective = 0
        self.is_hidden = is_hidden

        
class Col():
    def __init__(self, title="", width=Length(10, LenT.STAR), is_hidden=False, 
                 show_func: Callable[[Any], str] = None,
                 click_func: Callable[[Any], None] = None):
        self.title = title
        self.width = get_length(width)
        self.is_hidden = is_hidden or self.width.is_hidden
        self.show_func = show_func
        self.click_func = click_func
        pass
        
        
        
        
def get_length(length: Tuple|Length):
    tmp_len = None
    match length:
        case _ if isinstance(length, Length):
            tmp_len = length
        case _ if isinstance(length, tuple):
            v = length[0]
            s = length[1]
            hidden = False
            if len(length) >= 3:
                h = length[2]
                hidden = True if h == "h" else False
            eff_t = LenT.STAR if s == '*' else LenT.ABS
            tmp_len = Length(v, eff_t, hidden)
        case _:
            tmp_len = length
            
    return tmp_len
    
def get_lengths(len_list: list[Tuple|Length]):
    tmp_len_list = []
    for length in len_list:
        tmp_len = get_length(length)
        tmp_len_list.append(tmp_len)
    return tmp_len_list
    
def get_segments(len_list: list[Length], outer_len: int, test_list = []) -> list[Segment]:
    tmp_len_coll = get_lengths(len_list)
    star_sum = sum([l.value for l in tmp_len_coll if l.len_type == LenT.STAR])
    abs_sum = sum([l.value for l in tmp_len_coll if l.len_type == LenT.ABS])
    curr_effective = 0
    res_segments: list[Segment] = []
    
    star_available = max(0, outer_len - abs_sum)
    simple_lengths = []
    for length in tmp_len_coll:
        maybe_eff = length.value if length.len_type == LenT.ABS else int((star_available * length.value) / star_sum)
        if length.is_hidden:
            maybe_eff = 0
        length.effective = min(max(0, outer_len - curr_effective), maybe_eff)
        simple_lengths.append([length.effective, length.len_type == LenT.ABS, length.is_hidden])
        curr_effective += length.effective
    
    v_sum = sum([l[0] for l in simple_lengths])
    simple_stars = [l for l in simple_lengths if l[1] == False]
    diff = outer_len - v_sum
    if diff > 0  and len(simple_stars) > 0:
        last_star = simple_stars[-1]
        last_star[0] = last_star[0] + diff
    

    curr_effective = 0
    for simple_len in simple_lengths:
        segment = Segment(curr_effective, curr_effective + simple_len[0], simple_len[1])
        res_segments.append(segment)
        curr_effective += simple_len[0]

    return res_segments


