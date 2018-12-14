import sys

class ElveRecipes:
    def __init__(self):
        self.recipes = [3, 7]
        self.elves_idx = [0, 1]

    def step(self):
        score = sum([self.recipes[i] for i in self.elves_idx])
        new_recipes = [int(c) for c in str(score)]
        self.recipes.extend(new_recipes)
        self.elves_idx = [(e_idx + self.recipes[e_idx] + 1) % len(self.recipes) \
                            for e_idx in self.elves_idx]
        return new_recipes

    def __str__(self):
        return ' '.join(
            ['({})'.format(n) if i == self.elves_idx[0] else '[{}]'.format(n) if i == self.elves_idx[1] \
                else ' {} '.format(n) for i, n in enumerate(self.recipes)])

if __name__ == '__main__':
    input_num = open('../input/day14.in').readline().rstrip()

    ## First part
    num_recipes = int(input_num)
    elve_recipes = ElveRecipes()
    while len(elve_recipes.recipes) < num_recipes + 10:
        elve_recipes.step()

    print(''.join([str(n) for n in elve_recipes.recipes[num_recipes:num_recipes+10]]))

    ## Second part
    last_score = str(input_num)
    elve_recipes = ElveRecipes()
    while True:
        new_recipes = elve_recipes.step()
        possible_match = elve_recipes.recipes[-1 * (len(last_score) + len(new_recipes)): ]
        if last_score in ''.join([str(n) for n in possible_match]):
            break

    print(''.join([str(n) for n in elve_recipes.recipes]).index(last_score))