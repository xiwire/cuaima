import random


class Pattern:
    """ Sequence
    """
    def __init__(self, *args):
        self.index = 0
        self.collection = args

    def interpret(self):
        """ Interpret the pattern and return the next item in pattern
        TODO: recursively interpret patterns
        """
        return next(self)


class Lonely(Pattern):
    """ A workaround for lonely params
    """

    def __next__(self):
        return self.collection[0]


class Sequence(Pattern):
    """ Returns the next value in the collection every time, looping around
    once gotten to the end of the collection
    """
    def __next__(self):
        chosen = self.collection[self.index]
        self.index += 1
        self.index %= len(self.collection)
        return chosen


class Random(Pattern):
    """ Random choice among the patterned collection, can repeat the same value
    multiple times in a row
    """
    def __next__(self):
        chosen = random.choice(self.collection)
        return chosen
