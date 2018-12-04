import sys

# O(n * k)
# n being the number of IDs, and k the average length of each ID

lines = [l.rstrip() for l in sys.stdin.readlines()]
num_two_letters, num_three_letters = 0, 0
for line in lines:
    letters = dict()
    for c in line:
        if c not in letters:
            letters[c] = 0
        letters[c] += 1

    num_two_letters += 1 if 2 in letters.values() else 0
    num_three_letters += 1 if 3 in letters.values() else 0

print(num_two_letters * num_three_letters)
