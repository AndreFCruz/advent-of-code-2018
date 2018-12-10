import sys
import numpy as np

class Point:
    def __init__(self, init_pos, velocity):
        self.pos = init_pos
        self.vel = velocity

        self.second_count = 0

    def step(self):
        self.pos = [self.pos[i] + self.vel[i] for i in range(len(self.pos))]
        self.second_count += 1

    def step_backwards(self):
        self.pos = [self.pos[i] - self.vel[i] for i in range(len(self.pos))]
        self.second_count -= 1

def get_point_matrix(points):
    x_coords = [p.pos[0] for p in points]
    y_coords = [p.pos[1] for p in points]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    matrix = np.zeros((max_x - min_x + 1, max_y - min_y + 1), dtype=np.int8)
    for p in points:
        matrix[p.pos[0] - min_x, p.pos[1] - min_y] = 1

    return matrix

def print_message(points):
    point_matrix = get_point_matrix(points).T
    for x in range(len(point_matrix)):
        for y in range(len(point_matrix[x])):
            print('.' if point_matrix[x, y] == 0 else '#', end='')
        print(end='\n')

def check_message(points):
    """
    Assumes message is shown at the point of maximum convergence
     (when the points are closer together).
    """
    min_delta_x = -1

    while True:
        x_coords = [p.pos[0] for p in points]
        delta_x = max(x_coords) - min(x_coords)

        if delta_x < min_delta_x or min_delta_x == -1:
            min_delta_x = delta_x
        else: # Convergance reached (previous state was the message state)
            [p.step_backwards() for p in points]
            print_message(points)
            print('Second count: {}'.format(points[0].second_count))
            break

        for p in points:
            p.step()

if __name__ == '__main__':
    import re
    lines = [l.rstrip() for l in sys.stdin.readlines()]
    matches = [re.match(r'position=<([-\s]\d+), ([-\s]\d+)> velocity=<([-\s]\d+), ([-\s]\d+)>', l) for l in lines]
    
    points = [Point([int(m.group(1)), int(m.group(2))], [int(m.group(3)), int(m.group(4))]) for m in matches]

    ## First and second parts
    check_message(points)
