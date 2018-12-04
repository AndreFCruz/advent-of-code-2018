import sys

lines = sys.stdin.readlines()
freq_changes = list(map(lambda s: int(s.rstrip()), lines))

idx = 0
current_freq = 0
seen_freqs = set()  # Hash-set, O(1) insert and lookup
while True:
    if idx >= len(freq_changes):
        idx = 0
    current_freq += freq_changes[idx]
    if current_freq in seen_freqs:
        print(current_freq)
        break
        
    seen_freqs.add(current_freq)
    idx += 1