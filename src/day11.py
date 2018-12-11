import sys
import numpy as np
from scipy.signal import convolve2d


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

def get_max_grouping(matrix, group_size=(3,3)):
    """
    Returns the maximum 
    """
    filtered = convolve2d(matrix, np.ones(group_size, dtype=np.int), mode='valid')
    indices = np.unravel_index(np.argmax(filtered), filtered.shape)
    return indices, filtered[indices]

def get_max_variable_size_grouping(matrix):
    max_val = None
    max_side = None
    max_indices = None
    for i in range(1, 301):  # Should be up to 300
        indices, val = get_max_grouping(matrix, (i, i))
        if max_side is None or val > max_val:
            max_val = val
            max_side = i
            max_indices = indices
        elif val < 0:
            break

    return max_indices, max_side, max_val
        


if __name__ == '__main__':
    grid_serial_num = int(sys.stdin.readline().rstrip())
    GRID_SHAPE = (300, 300)

    ## First part
    grid = make_fuel_grid(GRID_SHAPE, grid_serial_num)
    max_square_idx, _ = get_max_grouping(grid)

    ## Add +1 to each coordinate to convert 0-indexed to 1-indexed
    print('{},{}'.format(* (max_square_idx[0] + 1, max_square_idx[1] + 1)))

    ## Second part
    indices, side, _ = get_max_variable_size_grouping(grid)
    print('{},{},{}'.format(* (indices[0] + 1, indices[1] + 1, side)))
