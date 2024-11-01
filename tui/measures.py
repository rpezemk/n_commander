from enum import Enum
from typing import Tuple

class Segment():
    def __init__(self, v0 = 0, v1 = 0):
        self.v0 = v0
        self.v1 = v1
    
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
    def __init__(self, value: int, len_type: LenT = LenT.STAR):
        self.value = value
        self.len_type = len_type
        self.effective = 0


def get_length(length: Tuple|Length):
    tmp_len = None
    match length:
        case _ if isinstance(length, Length):
            tmp_len = length
        case _ if isinstance(length, tuple):
            v = length[0]
            s = length[1]
            eff_t = LenT.STAR if s == '*' else LenT.ABS
            tmp_len = Length(v, eff_t)
        case _:
            tmp_len = length
            
    return tmp_len
    
def get_lengths(len_list: list[Tuple|Length]):
    tmp_len_list = []
    for length in len_list:
        tmp_len = get_length(length)
        tmp_len_list.append(tmp_len)
    return tmp_len_list
    
def get_segments(len_list: list[Length], outer_len: int) -> list[Segment]:
    tmp_len_coll = get_lengths(len_list)
    star_sum = sum([l.value for l in tmp_len_coll if l.len_type == LenT.STAR])
    curr_effective = 0
    res_lengths: list[Segment] = []
    
    for length in tmp_len_coll:
        maybe_eff = length.value if length.len_type == LenT.ABS else int(outer_len * (length.value / star_sum))
        length.effective = min(max(0, outer_len - curr_effective), maybe_eff)
        segment = Segment(curr_effective, curr_effective + length.effective)
        res_lengths.append(segment)
        curr_effective += length.effective
    
    v_sum = sum([s.v1 - s.v0 for s in res_lengths])
    if outer_len > v_sum:
        last = res_lengths[-1]
        last.v1 += outer_len - v_sum
    return res_lengths