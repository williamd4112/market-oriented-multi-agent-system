import numpy as np

from simulator.time_sys import TimeSystem
from simulator.city_graph import CityGraph
from simulator.city_customer_call_simulation import CityCustomerCallSimulation
 
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

        self.customer_call_sim = CityCustomerCallSimulation(self.intersections, self.city_graph)
              
    def step(self):
        # Setup the hyperparamters according to current time
        self.customer_call_sim.set(lambd=3)     

        # Generate customers' calls with the city_graph.
        customer_calls = self.customer_call_sim()
        for c in customer_calls:
            print(c)

        # Submitting all customers' calls to the taxi-coordinator

        # Shift taxi drivers
        pass
        
