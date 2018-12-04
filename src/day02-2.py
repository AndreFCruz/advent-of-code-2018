import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

## O(n^2 * k)
## n being the number of IDs, and k the average ID length
for i in range(len(lines)):
    for j in range(i + 1, len(lines)):
        different_chars = set()

        assert len(lines[i]) == len(lines[j])
        for idx in range(len(lines[i])):
            if lines[i][idx] != lines[j][idx]:
                different_chars.add(idx)
            if len(different_chars) > 1:
                break

        if len(different_chars) == 1:
            idx = different_chars.pop()
            print(lines[i][:idx] + lines[i][idx+1:])
            exit()
