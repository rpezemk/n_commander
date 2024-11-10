from dataclasses import dataclass


class TuiSet():
    def __init__(self, *args: list[str]):
        self.horizontal =   args[0]
        self.vertical =     args[1]
        self.top_left =     args[2]
        self.top_right =    args[3]
        self.bottom_left =  args[4]
        self.bottom_right = args[5]
        self.upper_conn = args[6]
        self.lower_conn = args[7]
        self.cross = args[8]
        self.left_conn = args[9]
        self.right_conn = args[10]
        self.dash_h = args[11]
        self.dash_v = args[12]
        self.arr_l = args[13]
        self.arr_u = args[14]
        self.arr_r = args[15]
        self.arr_d = args[16]
        pass


up_arrow = "\u2191"
dn_arrow = "\u2193"
double_up_arrow = "\u21D1"
double_dn_arrow = "\u21D3"
double_left_arrow = "\u21D0"
double_right_arrow = "\u21D2"

@dataclass
class TS():
    d = TuiSet("\u2550", "\u2551", "\u2554", "\u2557", 
               "\u255A", "\u255D", "\u2566", "\u2569", 
               "\u256c", "\u2560", "\u2563", "\u2505", 
               "\u2563", 
               double_left_arrow, double_up_arrow, double_right_arrow, double_dn_arrow)
    
    s = TuiSet("\u2500", "\u2502", "\u250C", "\u2510", 
               "\u2514", "\u2518", "\u252c", "\u2534",  
               "\u253c", "\u251c", "\u2524", "\u2504", 
               "\u250a", 
               double_left_arrow, double_up_arrow, double_right_arrow, double_dn_arrow)
