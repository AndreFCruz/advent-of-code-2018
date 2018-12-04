import sys
import re

FABRIC_SIDE = 1000

lines = [l.rstrip() for l in sys.stdin.readlines()]
fabric = [[0 for _ in range(FABRIC_SIDE)] for _ in range(FABRIC_SIDE)]

for line in lines:
    match = re.match(r'#([\d]+) @ ([\d]+),([\d]+): ([\d]+)x([\d]+)', line)
    claim_id    = int(match.group(1))
    from_left   = int(match.group(2))
    from_right  = int(match.group(3))
    width       = int(match.group(4))
    height      = int(match.group(5))

    for row in range(from_right, from_right + height):
        for col in range(from_left, from_left + width):
            fabric[row][col] += 1

print(sum([1 if n > 1 else 0 for l in fabric for n in l]))
