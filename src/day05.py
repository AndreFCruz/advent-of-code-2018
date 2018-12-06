import sys

line = sys.stdin.readline().rstrip()

# O(n^2), as string manipulation is O(n)
def perform_reactions(string):
    i = 0
    while i < len(string) - 1:
        if string[i].upper() == string[i+1].upper() and string[i] != string[i+1]:
            string = string[:i] + string[i+2:]
            i -= 1
        else:
            i += 1

    return string

# O(n) attempt by modifying the string in place instead of creating a new one at each iteration
def perform_reactions_in_place(string):
    def find_nearest(li, condition, start, end, step=1):
        for i in range(start, end, step):
            if condition(li[i]):
                return i
        return -1

    s = [c for c in string] # Copy string to list, in order to modify in place
    i = 0
    while i < len(string) - 1:
        nearest_base = find_nearest(s, lambda c: c != '.', start=i+1, end=len(s), step=1)
        if nearest_base == -1:
            break
        if s[i] != '.' and s[i].upper() == s[nearest_base].upper() and s[i] != s[nearest_base]:
            s[i], s[nearest_base] = '.', '.' # Mark to be removed
            i = find_nearest(s, lambda c: c != '.', start=i-1, end=-1, step=-1)
        else:
            i = find_nearest(s, lambda c: c != '.', start=i+1, end=len(s), step=1)

    return ''.join(filter(lambda c: c != '.', s))

def shortest_polymer(string, perform_reactions_func=perform_reactions):
    lengths = list()
    for base in set(string.upper()):
        s = list(filter(lambda c: c.upper() != base, string))
        lengths.append(len(perform_reactions_func(s)))
        # print('base "{}": {}'.format(base, lengths[-1]))
    return min(lengths)

# First part
print(len(perform_reactions_in_place(line)))

# Second part
print(shortest_polymer(line, perform_reactions_in_place))