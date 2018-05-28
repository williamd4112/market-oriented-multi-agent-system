from simulator.city_graph import CityGraph

if __name__ == '__main__':
    intersections = [ 
	    # (x,y) is the place of a intersection
        (0,0), (0,2), (0,6), (0,8), (0,12), (0,14),
        (2,0), (2,2), (2,6), (2,7), (2,8) , (2,12), (2,14),
        (3,0), (3,2), (3,6), (3,7), (3,8) , (3,12), (3,14),
        (4,0), (4,2), (4,4), (4,6), (4,7) , (4,8) , (4,12), (4,14),
        (5,0), (5,2), (5,4), (5,6), (5,8) , (5,12), (5,14),
        (7,0), (7,2), (7,4), (7,6), (7,8) , (7,12), (7,14),
    ]
    g = CityGraph(intersections)
    
    print(g.get_poses_on_distance(0, 3))    
    print(g.get_pos_shortest_distance((0, 0.5), (0, 2)))   
    print(g.get_pos_shortest_distance((0.5, 0.5), (0, 2)))
    print(g.get_pos_shortest_distance((0, 0), (0, 2)))
    print(g.get_pos_shortest_distance((0, 0), (0, 3)))
    print(g.get_pos_shortest_distance((0, 0), (1, 2)))
    print(g.get_pos_shortest_distance((0, 0), (0.5, 2)))
    print(g.get_pos_shortest_distance((0, 0), (0.5, 1)))
    print(g.get_pos_shortest_distance((0, 0), (5, 6)))
    print(g.get_pos_shortest_distance((0, 0), (3, 6)))
    print(g.get_pos_shortest_distance((2, 2), (0, 2)))   
    print(g.get_pos_shortest_distance((1, 2), (0, 2)))   
    print(g.get_pos_shortest_distance((1, 2), (0, 0)))   
    print(g.get_pos_shortest_distance((1, 2), (0, 0.1)))   
    
    
