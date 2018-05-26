import numpy as np

from util.graph import Graph
from util.common import check_duplicated_element

# TODO: Define in a common file
INF = int(1e9)

class CityGraph(Graph):
    DIRS =  [   (0, -1),# Left
                (-1, 0),# Up
                (0, 1), # Right
                (1, 0)  # Down
            ]

    def __init__(self, intersections):
        # Check duplicated intersection
        if check_duplicated_element(intersections):
            raise Exception("Error: duplicated interscetion.")

        # Find boundary
        min_i = min_j = INF
        max_i = max_j = -INF
        for pos in intersections:
            if pos[0] < min_i: min_i = pos[0]
            if pos[0] > max_i: max_i = pos[0]
            if pos[1] < min_j: min_j = pos[1]        
            if pos[1] > max_j: max_j = pos[1]     

        # Check boundary
        def _is_in_boundary(p):
            return (p[0] >= min_i and p[0] <= max_i and p[1] >= min_j and p[1] <= max_j)
        
        self.idx_table = {pos: idx for idx, pos in enumerate(intersections)}
        
        # Check bounds points
        if (min_i, min_j) not in self.idx_table or \
                (min_i, max_j) not in self.idx_table or \
                (max_i, min_j) not in self.idx_table or \
                (max_i, max_j) not in self.idx_table:
            raise Exception("Error: invalid intersections list")

        num_vertex = len(self.idx_table)
        
        # Initialize the length of each edge as INF
        adj_matrix = np.zeros([num_vertex, num_vertex], dtype=np.int32)
        adj_matrix.fill(INF)       
        
        # Set the length of each edge in the adj_matrix according to the intersections
        for pos in intersections:
            current_pos_idx = self.idx_table[pos]
            adj_matrix[current_pos_idx, current_pos_idx] = 0
            for d in CityGraph.DIRS:
                length = 1
                next_pos = (pos[0] + d[0] * length, pos[1] + d[1] * length)
                while _is_in_boundary(next_pos):
                    if next_pos in self.idx_table:
                        next_pos_idx = self.idx_table[next_pos]
                        adj_matrix[current_pos_idx, next_pos_idx] = length
                        break
                    length += 1
                    next_pos = (pos[0] + d[0] * length, pos[1] + d[1] * length)
        self.adj_matrix = adj_matrix.copy()
        super(CityGraph, self).__init__(adj_matrix)

    def get_id(self, pos):
        '''
        Retrieve an node ID of a position.
        '''               
        return self.idx_table[pos]
