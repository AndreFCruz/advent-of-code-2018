import sys
import numpy as np
import queue

class MapMatrix:
    UNCLAIMED_POINT = -1
    SAME_DISTANCE   = -2

    def __init__(self, coords):
        self.min_x, self.max_x = min([c[0] for c in coords]), max([c[0] for c in coords])
        self.min_y, self.max_y = min([c[1] for c in coords]), max([c[1] for c in coords])
        self.ids_map = {tuple(coords[i]): i for i in range(len(coords))}

        array_shape = (self.max_x - self.min_x + 2, self.max_y - self.min_y + 2)    # 1 pad at both ends to represent infinity
        self.distances = np.zeros(array_shape, dtype=int)
        self.coord_ids = np.zeros(array_shape, dtype=int) + MapMatrix.UNCLAIMED_POINT

        self.expand_queue = queue.Queue()

    def expand(self):
        for coord_pos, coord_id in self.ids_map.items():
            self.expand_at(coord_id, 0, coord_pos[0], coord_pos[1])

        while self.expand_queue.qsize():
            c_id, c_dist, x, y = self.expand_queue.get()
            self.expand_at(c_id, c_dist, x, y)

    def expand_at(self, coord_id, coord_dist, x, y):
        if self.is_out_of_bounds(x, y) or \
           self.get_coord_id_at(x, y) == coord_id:
            return
        
        other_id = self.get_coord_id_at(x, y)
        if other_id == MapMatrix.UNCLAIMED_POINT:   # Unclaimed space
            self.set_id_dist_at(x, y, coord_id, coord_dist)
            self.add_moves_to_queue(coord_id, coord_dist + 1, x, y)
            return

        other_dist = self.get_distance_at(x, y)
        # Claimed space, check if nearer to this coord
        if coord_dist == other_dist:
            self.set_id_dist_at(x, y, MapMatrix.SAME_DISTANCE, coord_dist)
        if coord_dist < other_dist:
            self.set_id_dist_at(x, y, coord_id, coord_dist)
            self.add_moves_to_queue(coord_id, coord_dist + 1, x, y)

    def add_moves_to_queue(self, coord_id, coord_dist, x, y):
        for p in MapMatrix.next_points(x, y):
            self.expand_queue.put((coord_id, coord_dist, p[0], p[1]))


    def is_out_of_bounds(self, x, y):
        m_x, m_y = self.get_matrix_pos(x, y)
        if m_x < 0 or m_x >= len(self.distances) or \
           m_y < 0 or m_y >= len(self.distances[m_x]):
            return True
        return False

    def set_id_dist_at(self, x, y, coord_id, dist):
        m_x, m_y = self.get_matrix_pos(x, y)
        self.coord_ids[m_x, m_y] = coord_id
        self.distances[m_x, m_y] = dist

    def get_distance_at(self, x, y):
        m_x, m_y = self.get_matrix_pos(x, y)
        return self.distances[m_x, m_y]

    def get_coord_id_at(self, x, y):
        m_x, m_y = self.get_matrix_pos(x, y)
        return self.coord_ids[m_x, m_y]

    def get_matrix_pos(self, x, y): # TODO check this
        return x - self.min_x + 1, y - self.min_y + 1

    def get_coord_id(self, x, y):
        return self.ids_map[(x, y)]

    @staticmethod
    def next_points(x, y, directions=((0,1),(0,-1),(1,0),(-1,0))):
        return [(x+d[0], y+d[1]) for d in directions]

    # @staticmethod
    # def distance(x1, y1, x2, y2):
    #     return abs(x2- x1) + abs(y2 - y1)

    def print(self): # Transpose (flip x/y) for printing
        for x in range(len(self.coord_ids)):
            for y in range(len(self.coord_ids[x])):
                print('{:3}'.format(self.coord_ids[x,y]), end='')
            print(end='\n')



if __name__ == '__main__':
    coords = [[int(coord) for coord in l.rstrip().split(', ')] for l in open('../input/day06.in').readlines()]

    matrix = MapMatrix(coords)
    matrix.expand()

    infinites = set()
    infinites |= set(np.unique(matrix.coord_ids[:, 0]))
    infinites |= set(np.unique(matrix.coord_ids[:, -1]))
    infinites |= set(np.unique(matrix.coord_ids[0, :]))
    infinites |= set(np.unique(matrix.coord_ids[-1, :]))
    # print(infinites)

    candidate_ids = set(matrix.ids_map.values()) - infinites
    areas = [np.count_nonzero(matrix.coord_ids == c_id) for c_id in candidate_ids]

    ## First part
    print(max(areas))

    ## Second part
    MAX_DIST_TO_COORD = 10000
    distance = lambda p1, p2: abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
    distance_sums = np.asarray(
        [[sum([distance((x, y), matrix.get_matrix_pos(c_x, c_y)) for c_x, c_y in matrix.ids_map.keys()]) \
            for y in range(len(matrix.distances[x]))] for x in range(len(matrix.distances))]
    )

    print(len(distance_sums[distance_sums < MAX_DIST_TO_COORD]))