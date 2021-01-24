SynthDef(\putOutStereo,
	/*
	A stereo output module, with built in limiter and compressor.
	*/
	{
		arg in_l=999, in_r=999, out=0;
		var bIn_l, bIn_r,
		    limiter, compressor;

		bIn_l = In.ar(in_l, 1);
		bIn_r = In.ar(in_r, 1);

		compressor = Compander.ar([bIn_l, bIn_r]);
		limiter = Limiter.ar(compressor);

		Out.ar(out, limiter);
	}
).add;

SynthDef(\mix6,
	/*
	6 channel mixer with two stereo sends.
	Sends are post-volume. Might change later.
	*/
	{
		arg in_1=999, in_1_lvl=1.0, in_1_send_a=1.0, in_1_send_b=1.0,
		    in_2=999, in_2_lvl=1.0, in_2_send_a=1.0, in_2_send_b=1.0,
		    in_3=999, in_3_lvl=1.0, in_3_send_a=1.0, in_3_send_b=1.0,
		    in_4=999, in_4_lvl=1.0, in_4_send_a=1.0, in_4_send_b=1.0,
		    in_5=999, in_5_lvl=1.0, in_5_send_a=1.0, in_5_send_b=1.0,
		    in_6=999, in_6_lvl=1.0, in_6_send_a=1.0, in_6_send_b=1.0,
		    send_a=999, return_a_l=999, return_a_r=999, return_a_lvl=1.0,
		    send_b=999, return_b_l=999, return_b_r=999, return_b_lvl=1.0,
		    out=0;
		var bIn_1, bIn_2, bIn_3, bIn_4, bIn_5, bIn_6,
		    return_a, return_b;

		bIn_1 = In.ar(in_1, 1) * in_1_lvl;
		bIn_2 = In.ar(in_2, 1) * in_2_lvl;
		bIn_3 = In.ar(in_3, 1) * in_3_lvl;
		bIn_4 = In.ar(in_4, 1) * in_4_lvl;
		bIn_5 = In.ar(in_5, 1) * in_5_lvl;
		bIn_6 = In.ar(in_6, 1) * in_6_lvl;

		Out.ar(send_a, Mix.ar([
			bIn_1 * in_1_send_a,
			bIn_2 * in_2_send_a,
			bIn_3 * in_3_send_a,
			bIn_4 * in_4_send_a,
			bIn_5 * in_5_send_a,
			bIn_6 * in_6_send_a
		]));

		Out.ar(send_b, Mix.ar([
			bIn_1 * in_1_send_b,
			bIn_2 * in_2_send_b,
			bIn_3 * in_3_send_b,
			bIn_4 * in_4_send_b,
			bIn_5 * in_5_send_b,
			bIn_6 * in_6_send_b
		]));

		return_a = In.ar([return_a_l, return_a_r], 2) * return_a_lvl;
		return_b = In.ar([return_b_l, return_b_r], 2) * return_a_lvl;

		Out.ar(out, Mix.ar([
			bIn_1!2,
			bIn_2!2,
			bIn_3!2,
			bIn_4!2,
			bIn_5!2,
			bIn_6!2,
			[return_a, return_a + 1],
			return_b
		]));
	}
).add;
