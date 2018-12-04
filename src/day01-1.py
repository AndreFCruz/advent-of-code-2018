import sys

lines = sys.stdin.readlines()
final_freq = sum(map(lambda s: int(s.rstrip()), lines))

print(final_freq, file=sys.stdout)