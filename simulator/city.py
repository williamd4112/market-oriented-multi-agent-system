import numpy as np
from simulator.time_sys import TimeSystem

#                   ((x,y), length of left/up/right/down edge)
INTERSECTIONS = [   ((0,0), -1, -1, 2, 2),
                    ((0,1), 2, -1, 4, 2),]


class CustomerCallsSimulation(object):
    def __init__(self, city_map):
        self.city_graph = self._convert_to_graph(city_map)
        

class City(object):
    def __init__(self, initial_hour, city_map):
        '''
        initial_hour: initial time
        city_map: a list of intersections
        '''
        self.time_system = TimeSystem(initial_hour)
        self.city_map = city_map
              
    def step(self):
        # Setup the hyperparamters according to current time
    
        # Generate customers' calls with the city_graph.

        # Submitting all customers' calls to the taxi-coordinator

        # Shift taxi drivers
        pass
        
