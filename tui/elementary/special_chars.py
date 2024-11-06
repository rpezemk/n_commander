import math

v_0 = ' '       # ' ' 
v_1 = '\u2581'  # '▁'
v_2 = '\u2582'  # '▂'
v_3 = '\u2583'  # '▃'
v_4 = '\u2584'  # '▄'
v_5 = '\u2585'  # '▅'
v_6 = '\u2586'  # '▆'
v_7 = '\u2587'  # '▇'
v_8 = '\u2588'  # '█'

vertical = [v_0, v_1, v_2, v_3, v_4, v_5, v_6, v_7, v_8]
n_v = len(vertical)
t_v = (n_v, vertical)

h_0 = ' '       #' '
h_1 = '\u258F'  #'▏'
h_2 = '\u258E'  #'▎'
h_3 = '\u258D'  #'▍'
h_4 = '\u258C'  #'▌'
h_5 = '\u258B'  #'▋'
h_6 = '\u258A'  #'▊'
h_7 = '\u2589'  #'▉'
h_8 = '\u2588'  #'█'
    
horizontal = [h_0, h_1, h_2, h_3, h_4, h_5, h_6, h_7, h_8]
n_h = len(horizontal)
t_h = (n_h, horizontal)

s_0 = ' '       # ' '
s_1 = '\u2591'  # '░'
s_2 = '\u2592'  # '▒'
s_3 = '\u2593'  # '▓'
s_4 = '\u2588'  # '█'
shades = [s_0, s_1, s_2, s_3, s_4]

n_s = len(shades)
t_s = (n_s, shades)


h_rod_0 = ' '          # ' ' 
h_rod_1 = '\U0001D360' # '𝍠'
h_rod_2 = '\U0001D361' # '𝍡'
h_rod_3 = '\U0001D362' # '𝍢'
h_rod_4 = '\U0001D363' # '𝍣'
h_rod_5 = '\U0001D364' # '𝍤'

v_rods = [h_rod_0, h_rod_1, h_rod_2, h_rod_3, h_rod_4, h_rod_5]
n_v_rods = len(v_rods)
t_v_rods = (n_v_rods, v_rods)

v_rod_0 = ' '          # 
v_rod_1 = '\U0001D369' # 
v_rod_2 = '\U0001D36A' # 
v_rod_3 = '\U0001D36B' # 
v_rod_4 = '\U0001D36C' # 

h_rods = [v_rod_0, v_rod_1, v_rod_2, v_rod_3, v_rod_4]
n_h_rods = len(h_rods)
t_h_rods = (n_h_rods, h_rods)


def map_fract_to_char(fract: float, t: list[str]) -> str:
    chars = t[1]
    max_idx = t[0] - 1
    idx = math.ceil(min(1, fract) * max_idx)
    res = chars[idx]
    return res



def get_h_bar(n_chars: int, max_val: float, val: float):
    real_width = n_chars * val/max_val
    n_full = int(real_width)
    if n_full == n_chars:
        return v_rod_4 * n_full
    n_empty = int(n_chars - real_width)
    fract = real_width - n_full # is segment [0, 1)
    last = map_fract_to_char(fract, t_h_rods)
    res = v_rod_4 * n_full + last + ' ' * (n_chars - n_full - 1)
    return res

def get_v_bar(n_chars: int, max_val: float, val: float):
    real_width = n_chars * val/max_val
    n_full = int(real_width)
    if n_full == n_chars:
        return v_8 * n_full
    n_empty = int(n_chars - real_width)
    fract = real_width - n_full # is segment [0, 1)
    last = map_fract_to_char(fract, t_v)
    res = v_8 * n_full + last + ' ' * (n_chars - n_full - 1)
    return res

# for i in range(0, 101):
#     bar = get_v_bar(5, 100, i)
#     l = len(bar)
#     print(bar + " " + str(l))