from jinja2 import Template

options = "-odac"

gen_instrument = """
instr 1
    a1 oscili 0.5, 440
    outs a1, a1
    event_i "i", 2, 5, p3
endin
"""

closing_instrument = """instr 2
    exitnow  ; 
endin"""

csd = """
<CsoundSynthesizer>
<CsOptions>
{{ options }}
</CsOptions>

<CsInstruments>

; Initialize the Csound orchestra
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1
{% for instr in instruments %}{{ instr }}\n{% endfor %}
</CsInstruments>
<CsScore>
{% for event in events %}    {{ event }} {% endfor %}
</CsScore>
</CsoundSynthesizer>

"""

events = ["i 1 0 10"]

def get_instr():
    template = Template(csd)
    render = template.render(options=options, instruments = [gen_instrument, closing_instrument], events=events)
    return render
