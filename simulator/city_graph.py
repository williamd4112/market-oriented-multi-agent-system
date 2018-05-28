import numpy as np

from collections import deque as Queue

from util.graph import Graph
from util.common import check_duplicated_element, movement_to_dir

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
        self.idx_to_pos_table = {idx: pos for pos, idx in self.idx_table.items()}
        
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

    def get_pos(self, idx):
        '''
        Retrieve a node's position by id
        '''
        return self.idx_to_pos_table[idx]

    def get_shortest_distance(self, u, v):
        '''
        Retrieve the shortest distance between node u and v
        '''
        return self.distance_matrix[u, v]        

    def get_shortest_path(self, u, v):
        '''
        Retrieve the shortest path a list of positions from node u to v
        '''
        return self.get_path(u, v)

    def get_poses_on_distance(self, start_node_idx, distance):
        '''
        Retrieve a list of positions of which distances to start_node equal to the given distance.
        '''
        nodes = self.get_nodes_with_distance(start_node_idx, distance)
        poses = []
        for node in nodes:
            # Check if it can find a position on the lines connected to start_node_idx
            distance_to_node = self.get_shortest_distance(start_node_idx, node)
            node_pos = self.get_pos(node)
            residual_distance = distance - distance_to_node
            neighbor_nodes, neighbor_node_distances = self._get_all_neighbor_nodes(node)
            for neighbor_node, neighbor_node_distance in zip(neighbor_nodes, neighbor_node_distances):
                if (residual_distance < neighbor_node_distance):
                    neighbor_node_pos = self.get_pos(neighbor_node)
                    relative_movement = (neighbor_node_pos[0] - node_pos[0], neighbor_node_pos[1] - node_pos[1])
                    direction = movement_to_dir(relative_movement)                     
                    pos = (node_pos[0] + direction[0] * residual_distance, node_pos[1] + direction[1] * residual_distance)                
                    # Check if we can travel to pos with shorter distance from the other side
                    distance_start_to_the_other_side = self.get_shortest_distance(start_node_idx, neighbor_node)
                    distance_the_other_side_to_pos = distance_start_to_the_other_side + (neighbor_node_distance - residual_distance)
                    if distance_to_node + residual_distance <= distance_the_other_side_to_pos:
                        poses.append(pos)                        
        return list(set(poses))
    
    def get_nodes_with_distance(self, start_node_idx, distance):
        '''
        Retrieve a list of nodes of which distance to start_node is within the given distance.
        '''
        nodes = []
        for v in range(len(self.distance_matrix)):
            if self.distance_matrix[start_node_idx, v] <= distance:
                nodes.append(v)              
        return nodes

    def _get_all_neighbor_nodes(self, node_idx):
        '''
        Return a list of indexes of neighbor nodes and a list of distance to neighbor nodes.
        '''
        neighbor_nodes = []
        neighbor_nodes_distance = []
        for v in range(len(self.adj_matrix[node_idx])):
            if self.adj_matrix[node_idx, v] < INF and v != node_idx:
                neighbor_nodes.append(v)
                neighbor_nodes_distance.append(self.adj_matrix[node_idx, v])
        return neighbor_nodes, neighbor_nodes_distance
    


