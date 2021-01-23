# CUAIMA

**WORK IN PROGRESS: _HERE BE DRAGONS_**
*The contents of this README may reflect functionality that is not yet
implemented*

CUAIMA is a live coding DSL for sound manipulation implemented in Python. It's
inspired by modular synthesizers and tries to be quick and easy to use while
offering a variety of different approaches to making sound.

## Why?

I've spent about two years playing with TidalCycles and before that, I only
used plain SuperCollider. During this time, I started getting into making
electronic music, started building a modular synthesizer and have gone through
a pile of synths and samplers. Through this experience I've gained a better
understading of what I want from a live coding language. CUAIMA is an attempt
of implementing some ideas I've had for a long time and bridge the gap between
what's on my mind and what I'm capable of.

On the other hand, I think that using other people's tools can be an obstacle
to creativity, conditioning the way that you think and approach creation. I
believe I can only make the music I want in the way I want if I make my own
tools.

## Making sound

Cuaima provides you with two main interfaces to generate sound: patterns and
connections.

### Patterns

Patterns are what you are probably most used to. Languages like Sonic Pi,
TidalCycles, FoxDot, Gibber, etc, all work with different abstractions on
patterns.  They are a pretty useful way to think about most kinds of popular
music.

Patterns in CUAIMA are based on SuperCollider patterns, here's an example:
```python
# we first instatiate a synth we want to play
synth = Biast()  

# then we schedule it to be called in a particular way
sched(
  synth,  # the first argument is always the synth to play with
  beat=1,  # beat is a special argument that tells it how often to play, it can
           # also be a pattern!
  freq=seq(220, 440, 880),  # seq cycles through its arguments linearly,
                            # looping back when it has run through all of them
  harmonic=rand(0.2, 0.4),  # rand cycles through its arguments randomly
)
```
In this code example, `seq` and `rand` are patterns.

### Connections

Connections utilizes Buses in SuperCollider in a way inspired by modular synths
to gain more flexibility in the ways to work with sound.

```python
output = PutOutStereo()  # an output module
mixer = Mix6()           # a 6-channel mixer
reverb = VerbFree()      # a stereo reverb
biast = Biast()          # a synth voice
quad_lfo = QuadLFO()     # a modulation source

# we connect the output of the synth voice to the mixer's first input
biast.out > mixer.in_a

# we use the mixer's sends to add some reverb
mixer.send_a > reverb.in_l 

# connection direction doesn't matter and multichannel inputs and outputs are
# handled automatically
mixer.return_a < reverb.out  

# we can modulate any control parameter of any module with any control rate
# modulation source
quad_lfo.sine_1 > biast.harmonic

# we finally take the mixer's output to the output module's input and now we
# can get sound when we play the Biast module
mixer.out > output.in

# we can mix and match patterns with connections and use python idioms
sched(biast, beat=1/4, penv=seq(1, *[0]*3)

# we can use patterns to modulate any control rate parameters
sched(quad_lfo, sine_1_freq=rand(*[i * 100 for i in range(0, 10)]))
```

## How to use it
CUAIMA is bundled as a Python library, so you can use it by cloning this
repository and installing it via pip:

```shell
git clone https://github.com/jxpp/cuaima
cd cuaima

# if you dont have pipenv
pip install --user .

# or if you have pipenv
pipenv install
pipenv shell
```

Then you can just run `from cuaima.dsl import *` on a Python REPL to get the
main functions to get you started.

I use NeoVim along with [vim-slime](https://github.com/jpalardy/vim-slime) to
use it.
