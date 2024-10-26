from enum import Enum

class HPosEnum(Enum):
    LEFT = 1
    RIGHT = 2
    STRETCH = 3
    AUTO = 4


class VPosEnum(Enum):
    TOP = 1
    BOTTOM = 2
    STRETCH = 3
    AUTO = 4
    

class PanelPlacement():
    def __init__(self, vPos: VPosEnum = VPosEnum.TOP, hPos: HPosEnum = HPosEnum.LEFT):
        self.vPos = vPos
        self.hPos = hPos
        pass    
    
class GPlace():
    def __init__(self, row_no: int, row_span: int, col_no: int, col_span: int):
        self.row_no = row_no
        self.row_span = row_span
        self.col_no = col_no
        self.col_span = col_span
        pass
    