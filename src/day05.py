import sys

line = sys.stdin.readline().rstrip()

# O(n^2), as string manipulation is O(n) in the size of the string
def perform_reactions(string):
    i = 0
    while i < len(string) - 1:
        if string[i].upper() == string[i+1].upper() and string[i] != string[i+1]:
            string = string[:i] + string[i+2:]
            i -= 1
        else:
            i += 1

    return string

def shortest_polymer(string):
    lengths = list()
    for base in set(string.upper()):
        s = list(filter(lambda c: c.upper() != base, string))
        lengths.append(len(perform_reactions(s)))
        # print('base "{}": {}'.format(base, lengths[-1]))
    return min(lengths)

print(len(perform_reactions(line)))
print(shortest_polymer(line))