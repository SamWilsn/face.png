#!/usr/bin/env python3

from numpy import packbits
from png import Reader
import sys


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


reader = Reader(filename=sys.argv[1])
width, height, values, _ = reader.read_flat()
scanlines = [bytes(packbits(line)).hex() for line in chunks(values, width)]

for line in scanlines[:-1]:
    print(f'        hex"{line}"')

print(f'        hex"{line}";')
