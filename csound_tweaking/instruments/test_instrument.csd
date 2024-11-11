<CsoundSynthesizer>
<CsOptions>
; Use appropriate audio output options for your setup
-odac
</CsOptions>

<CsInstruments>

; Initialize the Csound orchestra
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
    a1 oscili 0.5, 440
    outs a1, a1
    event_i "i", 2, 5, p3
endin

instr 2
    exitnow  ; 
endin

</CsInstruments>

<CsScore>

i 1 0 10
</CsScore>

</CsoundSynthesizer>
