import numpy as np

from util.defines import INF

class Graph(object):
    def __init__(self, graph):
        num_vertex = len(graph)

        p = np.zeros(graph.shape)
        for i in range(0, num_vertex):
            for j in range(0, num_vertex):
                p[i,j] = i
                if (i != j and graph[i,j] == 0): 
                    p[i,j] = -INF 
                    graph[i,j] = INF # set zeros to any large number which is bigger then the longest way

        for k in range(0, num_vertex):
            for i in range(0, num_vertex):
                for j in range(0, num_vertex):
                    if graph[i,j] > graph[i,k] + graph[k,j]:
                        graph[i,j] = graph[i,k] + graph[k,j]
                        p[i,j] = p[k,j]
        self.distance_matrix = graph
        self.predessor_matrix = p

    def get_path(self, i, j):
        i, j = int(i), int(j)
        if i == j:
            return [i]
        elif self.predessor_matrix[i,j] == -INF:
            return [None]
        else:
            preds = self.get_path(i, self.predessor_matrix[i,j]);
            return preds + [j]

if __name__ == '__main__':
    graph = np.array([[0,10,20,30,0,0],[0,0,0,0,0,7],[0,0,0,0,0,5],[0,0,0,0,10,0],[2,0,0,0,0,4],[0,5,7,0,6,0]])
    g = Graph(graph)


        
        
        
