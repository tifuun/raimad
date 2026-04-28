#!/usr/bin/env python3
from pathlib import Path
import re

file = Path('./src/raimad/cif/raidithers/carrot.xbm')

pxre = re.compile(r'0x([0-9a-f][0-9a-f])')
xbm = file.read_text()
arr = []
for px8 in pxre.findall(xbm):
    print(px8)
    px8 = int(px8, 16)
    for x in range(8):
        arr.append(int(bool(px8 & (1 << x))))

assert len(arr) == 32 ** 2, len(arr)

for row in range(0, 32):
    for col in range(0, 32 - row - 1):
        arr[(31 - col) * 32 + (31 - row)] = arr[row * 32 + col]
        #arr[row * 32 + col] = 1

px82 = []
while arr:
    n = 0
    for x in range(8):
        n |= arr.pop(0) << x
    px82.append(n)

assert len(px82) == 32 ** 2 / 8

xbm2 = pxre.sub(lambda _: hex(px82.pop(0)), xbm)
print(xbm2)

assert len(px82) == 0

file.with_suffix('.new.xbm').write_text(xbm2)

