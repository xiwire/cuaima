from cuaima.dsl import *


reverb = VerbFree()

sine = Sine()

sine.set(out=0, freq=200)

sched(sine, beat=1, freq=Random(220, 440, 880))

sine.ports


reverb.in_l < sine.out

sine_lfo = SineLFO()

sine_lfo.out > sine.phase

sine_lfo.set(freq=1200)

reverb.set(out_l=STDOUT)
