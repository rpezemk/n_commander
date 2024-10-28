import textwrap
from datetime import datetime

from tui.placements import GPlace
from tui.controls import Panel

class TBox(Panel):
    def __init__(self, title = "textBox", wrap=True, g_place=GPlace(0, 1, 0, 1)):
        super().__init__(title, g_place=g_place)
        self.text = ""
        
    def log(self, message):
        d = datetime.now()
        ms = int(d.microsecond / 1000)
        now = d.strftime("%Y-%m-%d %H:%M:%S") + "." + str(ms).rjust(3, "0")
        self.text += f"[{now}] {message}\n"
        
    def draw(self) -> None:
        h, w = self.area.get_dims()
        line_width = w - 4
        v_capacity = h - 1
        if line_width < 1 or v_capacity < 1:
            return
        
        win = self.emit_window()

        maybe_last_lines = self.text.split("\n")[-v_capacity:]
        real_last_lines: list[str] = []
        for line in maybe_last_lines:
            first_sub_line = line[:line_width]
            real_last_lines.append(first_sub_line)
            
            line_rest = line[line_width:]
            if line_rest == '':
                continue
            rest = "\n".join(textwrap.wrap(line_rest, width=line_width - 2))
            wrapped = textwrap.indent(rest, prefix="\\ ").split("\n")
            for sub_line in wrapped:
                real_last_lines.append(sub_line)
        
        for idx, line in enumerate(real_last_lines[-v_capacity:]):
            win.addstr(1 + idx, 2, line)
        win.refresh()
