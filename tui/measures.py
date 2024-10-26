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
        return self.y1 - self.y0, self.x1 - self.x0
    
class LenT(Enum):
    ABS = 1
    STAR = 2

class Len():
    def __init__(self, value: int, len_type: LenT = LenT.STAR):
        self.value = value
        self.len_type = len_type
        self.effective = 0
        
    
def get_effective_lengths(len_coll: list[Len], outer_len: int) -> list[Segment]:
    star_sum = sum([l.value for l in len_coll if l.len_type == LenT.STAR])
    curr_effective = 0
    res_lengths: list[Segment] = []
    
    for length in len_coll:
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