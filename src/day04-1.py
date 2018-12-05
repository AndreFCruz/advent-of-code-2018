import sys
import re
from datetime import datetime

# lines = [l.rstrip() for l in sys.stdin.readlines()]
lines = [l.rstrip() for l in open('input/day04.in').readlines()]
matches = list(map(lambda l: re.match(r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (Guard #(\d+) .*|falls .*|wakes .*)', l), lines))
dates = {datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))) : m for m in matches}

guards_schedule = dict()
start, end = -1, -1
for date, match in sorted(dates.items()):
    # import ipdb; ipdb.set_trace()    
    if match.group(7) is not None:  # New Guard entry
        guard_id = int(match.group(7))
        if guard_id not in guards_schedule:
            guards_schedule[guard_id] = [0 for _ in range(60)]
        continue

    if match.group(6) == 'falls asleep':
        start = int(match.group(5))
    elif match.group(6) == 'wakes up':
        end = int(match.group(5))
        for i in range(start, end):
            guards_schedule[guard_id][i] += 1

guard_most_asleep = max(guards_schedule, key=lambda k: sum(guards_schedule[k]))
minute_most_asleep = guards_schedule[guard_most_asleep].index(max(guards_schedule[guard_most_asleep]))

print(guard_most_asleep * minute_most_asleep)