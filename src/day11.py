import sys
import numpy as np
from scipy.signal import convolve2d

def get_max_grouping(matrix):
    """
    Returns the maximum 
    """
    filtered = convolve2d(matrix, np.ones((3, 3), dtype=np.int), mode='valid')
    return np.unravel_index(np.argmax(filtered), filtered.shape)

def make_fuel_grid(shape, grid_serial_num):
    grid = np.ndarray(shape, dtype=np.int)

    for x in range(1, grid.shape[0] + 1):
        for y in range(1, grid.shape[1] + 1):
            rack_id = x + 10
            power_level = rack_id * y + grid_serial_num
            power_level *= rack_id
            power_level = (power_level // 100) % 10 # Get 100's digit
            power_level -= 5
            grid[x-1, y-1] = power_level

    return grid


if __name__ == '__main__':
    grid_serial_num = int(open('../input/day11.in').readline().rstrip())
    GRID_SHAPE = (300, 300)

    ## First part
    grid = make_fuel_grid(GRID_SHAPE, grid_serial_num)
    max_square_idx = get_max_grouping(grid)
    print('{},{}'.format(* (max_square_idx[0] + 1, max_square_idx[1] + 1)))
