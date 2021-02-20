from enum import Enum


class Temperament(Enum):
    EQUAL = 'equal'
    WELL = 'well'
    MEAN_TONE = 'mean tone'
    PYTHAGOREAN = 'pythagorean'
    WERCKMEISTER_I
    WERCKMEISTER_II
    WERCKMEISTER_III
    WERCKMEISTER_IV


maj = (0, 4, 7)
minor = (0, 3, 7)
augmented = (0, 3, 8)
diminished = (0, 3, 6)
sus4 = (0, 5, 7)
sus2 = (0, 2, 7)
maj7 = (0, 4, 7, 9)
dom7 = (0, 3, 7, 9)


# A = 0
# Bb = As = 1
# B = 1
# C = 2
# Db = Cs =
# D = 3
# E = 4
# F = 5
# G = 6


def degree(temperament: Temperament = Temperament.EQUAL):
    pass


def chord(root: str, chord_type: tuple[int], inversion: int, octave: int = 3):
    return [degree(root + i) for i in chord_type]
