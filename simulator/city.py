import numpy as np

from simulator.time_sys import TimeSystem
from simulator.city_graph import CityGraph
from util.distribution import NormalDistribution, PoissonProcess
 
class City(object):
    def __init__(self, intersections, initial_hour, lambd_schedule):
        '''
        intersections: specification of intersections
        initial_hour: initial time
        lambd_schedule: schedule of lambda in Poisson process
        '''
        self.intersections = intersections
        self.city_graph = CityGraph(self.intersections)
        self.time_system = TimeSystem(initial_hour)

        self.poisson_process = PoissonProcess()
        self.normal_distribution = NormalDistribution()

    def _find_destination_with_distance(self, start_pos, distance):
        '''
        Retrieve a node of which distance to "start_pos" is close to a "distance" in the city_graph.
        '''
        # get a closet node in city_graph
        # complement the remaining distance        
        pos_closet_to_distance = self.city_graph.get
              
    def step(self):
        # Setup the hyperparamters according to current time
    
        # Generate customers' calls with the city_graph.
        for intersection in self.intersections:
            next_call_elapsed_time = self.poisson_process()
            travelling_distance = self.normal_distribution()
            destination = 

        # Submitting all customers' calls to the taxi-coordinator

        # Shift taxi drivers
        pass
        
