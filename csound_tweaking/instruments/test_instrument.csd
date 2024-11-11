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

; Define the instrument
instr 1
    ; Generate a sine wave
    a1 oscili 0.5, 440
    outs a1, a1

    ; Stop the Csound instance when this note ends
    event_i "i", 2, 0.5, p3  ; Trigger instrument 2 to stop Csound after this instrument ends
endin

; Define a stopping instrument
instr 2
    exitnow  ; This opcode immediately stops the Csound instance
endin

</CsInstruments>

<CsScore>
; Play instrument 1 for 2 seconds
i 1 0 2
</CsScore>

</CsoundSynthesizer>
