(
SynthDef(\verbFree,
	/*
	A stereo reverb effect
	TODO: write my own
	*/
	{
		arg in_l=999, in_r=999, 
            mix=1.0, room=0.4, damp=0.3,
		    out_l=999, out_r=999;
		Out.ar([out_l, out_r], FreeVerb.ar(In.ar([in_l, in_r], 2), mix: 1.0, room: 0.9, damp: 1.0));
	}
).add;
)
