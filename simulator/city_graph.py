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

        # Initialize the edges list
        edges = []
        for u in range(num_vertex):
            for v in range(u, num_vertex):      
                if u != v and self.adj_matrix[u, v] < INF:
                    edges.append((u, v))
        self.edges = edges
        super(CityGraph, self).__init__(adj_matrix)

    def get_id(self, pos):
        '''
        Retrieve an node ID of a position.
        '''               
        if pos not in self.idx_table: return None
        return self.idx_table[pos]

    def get_pos(self, idx):
        '''
        Retrieve a node's position by id
        '''
        if idx not in self.idx_to_pos_table: return None
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

    def get_pos_shortest_distance(self, pu, pv):
        '''
        Retrieve the shortest distance from pos pu to pv.
        Return None if the pos is not reacheable
        '''
        u_id = self.get_id(pu)
        v_id = self.get_id(pv)
        if u_id is None:
            possible_node_u = self._get_edge_with_pos(pu)
        else:
            possible_node_u = [u_id]

        if v_id is None:
            possible_node_v = self._get_edge_with_pos(pv)
        else:
            possible_node_v = [v_id]
       
        if possible_node_v is None or possible_node_u is None:
            return None        

        min_distance = INF
        for node_u in possible_node_u:        
            for node_v in possible_node_v:
                distance_node_u_to_node_v = self.get_shortest_distance(node_u, node_v)
                distance_node_v_to_pos_v = self._get_node_to_neighbor_pos_distance(node_v, pv)
                min_distance = min(min_distance, distance_node_u_to_node_v + distance_node_v_to_pos_v)
        return min_distance

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

    def _get_edge_with_pos(self, pos):
        for edge in self.edges:       
            i0, j0 = self.get_pos(edge[0])
            i1, j1 = self.get_pos(edge[1])
            # Horizontal edge
            if i0 == i1:
                min_j = min(j0, j1)
                max_j = max(j0, j1)
                if pos[0] == i0 and (pos[1] < max_j and pos[1] > min_j):
                    return list(edge)
            # Vertical edge
            elif j0 == j1:
                min_i = min(i0, i1)
                max_i = max(i0, i1)
                if pos[1] == j0 and (pos[0] < max_i and pos[0] > min_i):
                    return list(edge)
            else:
                raise Exception('Error: invalid edge.')

    def _get_node_to_neighbor_pos_distance(self, node, pos):
        node_pos = self.get_pos(node)               
        # Horizontal
        if node_pos[0] == pos[0]:
            distance = abs(pos[1] - node_pos[1])
        # Vertical
        elif node_pos[1] == pos[1]:
            distance = abs(pos[0] - node_pos[0])
        else:
            raise Exception('Error: invalid position.')
        
        if distance > self._get_max_neighbor_edge(node):
            raise Exception('Error: position is not in neighbor.')
        return distance
        
    def _get_max_neighbor_edge(self, node):
        max_len = -INF
        for l in self.adj_matrix[node]:
            if max_len < INF:
                max_len = max(max_len, l)
        return max_len
    


