import sys
import re

FABRIC_SIDE = 1000

lines = [l.rstrip() for l in sys.stdin.readlines()]
fabric = [['.' for _ in range(FABRIC_SIDE)] for _ in range(FABRIC_SIDE)]

non_intersected_claims = set()
for line in lines:
    match = re.match(r'#([\d]+) @ ([\d]+),([\d]+): ([\d]+)x([\d]+)', line)
    claim_id    = match.group(1)
    from_left   = int(match.group(2))
    from_right  = int(match.group(3))
    width       = int(match.group(4))
    height      = int(match.group(5))

    not_intersected = True
    for row in range(from_right, from_right + height):
        for col in range(from_left, from_left + width):
            if fabric[row][col] != '.':
                not_intersected = False
                other_claim = fabric[row][col]
                if other_claim in non_intersected_claims:
                    non_intersected_claims.remove(other_claim)
                fabric[row][col] = 'X'
            else:
                fabric[row][col] = claim_id

    if not_intersected:
        non_intersected_claims.add(claim_id)

print(non_intersected_claims.pop())