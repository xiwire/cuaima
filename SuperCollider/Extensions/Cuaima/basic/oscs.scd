(
SynthDef(\sine,
    {
        arg freq=440, phase=0, out=999;
        var sine;
        sine = SinOsc.ar(freq: freq, phase: phase);
        Out.ar(out, sine);
    }
).add;

SynthDef(\sineLFO,
    {
        arg freq=1, phase=0, amp=1, out=999;
        var sine;
        sine = SinOsc.kr(freq: freq, phase: phase, mul: amp);
        Out.kr(out, sine);
    }
).add;

SynthDef(\squareLFO,
    {
        arg freq=440, amp=1, out=999;
        var square;
        square = LFPulse.kr(freq: freq, mul: amp);
        Out.kr(out, square);
    }
).add;

SynthDef(\wnoise,
    {
        arg out=999;
        Out.ar(out, WhiteNoise.ar);
    }
).add;
)
