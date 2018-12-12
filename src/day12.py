import sys
import re

def iterate_once(state, rules):
    new_state = list()
    index_offset = state.index('#') - 3
    for i in range(index_offset, len(state) - state[::-1].index('#') + 3):
        if i < 2:
            current = ['.'] * (2-i) + state[:i+3]
        elif i >= len(state) - 2:
            current = state[i-2:] + ['.'] * (i - len(state) + 3)
        else:
            current = state[i-2:i+3]

        current = ''.join(current)
        if current in rules:
            new_state.append(rules[current])
        else:
            new_state.append('.')
            print('Current: ', current, ' not in rules')

    return new_state, index_offset

def iterate_plants(state, rules, iterations):
    index_of_first_elem = 0
    for i in range(iterations):
        state, index_offset = iterate_once(state, rules)
        index_of_first_elem += index_offset
    return state, index_of_first_elem

if __name__ == '__main__':
    lines = sys.stdin.readlines()

    initial_state = [c for c in lines[0][15:].rstrip()]
    rules = [re.match(r'([\.\#]+) => ([\.\#])', l) for l in lines[2:]]
    rules = {m.group(1) : m.group(2) for m in rules}
    assert rules['.....'] != '#', "pls no, infinite plants"

    ## First part
    NUM_ITERATIONS = 20
    final_state, idx_first_elem = iterate_plants(initial_state, rules, NUM_ITERATIONS)
    print(sum([i + idx_first_elem for i in range(len(final_state)) if final_state[i] == '#']))


    ## Second part
    # NUM_ITERATIONS = 50000000000
    # final_state, idx_first_elem = iterate_plants(initial_state, rules, NUM_ITERATIONS)
    # print(sum([i + idx_first_elem for i in range(len(final_state)) if final_state[i] == '#']))