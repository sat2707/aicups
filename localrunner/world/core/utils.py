import math
from itertools import chain
from random import randint, shuffle
from itertools import cycle


def range_generator(min, max):
    prev = 1467632017.0
    m = 2147483647.0
    k = 16807.0
    b = 0.0

    while True:
        prev = (k * prev + b) % m

        delta = int((math.floor(prev * max / m) + min) % (max + 1))
        from_floor = randint(min, max - delta)
        if randint(0, 1):
            yield from_floor, (from_floor + delta)
        else:
            yield (from_floor + delta), from_floor


def group_size_generator(sizes):
    sizes = list(chain(*[[k for _ in range(0, v)] for k, v in sizes.iteritems()]))
    shuffle(sizes)
    for i in cycle(sizes):
        yield i


def sign(x):
    if x < 0:
        return -1
    return 1

