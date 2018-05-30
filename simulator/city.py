import numpy as np

from simulator.time_sys import TimeSystem
from simulator.city_graph import CityGraph
from simulator.city_customer_call_simulation import CityCustomerCallSimulation
 
class City(object):
    def __init__(self, intersections, initial_hour, lambd_schedule=[]):
        '''
        intersections: specification of intersections
        initial_hour: initial time
        lambd_schedule: schedule of lambda in Poisson process
        '''
        self.intersections = intersections
        self.lambd_schedule = lambd_schedule
        self.city_graph = CityGraph(self.intersections)
        self.time_sys = TimeSystem(initial_hour)
        
        self.customer_call_sim = CityCustomerCallSimulation(self.intersections, self.city_graph, self.time_sys)
              
    def step(self):
        # Default lambd is 1.0
        self.customer_call_sim.set(lambd=1.0)
        current_hour_in_day = self.time_sys.hour_in_a_day()
        for start_hour_in_day, end_hour_in_day, lambd in self.lambd_schedule:
            if current_hour_in_day >= start_hour_in_day and current_hour_in_day < end_hour_in_day:
                self.customer_call_sim.set(lambd=lambd)
                break     

        # Generate customers' calls with the city_graph.
        customer_calls = self.customer_call_sim()

        # Accumulate the time
        self.time_sys.step()

        return sorted(customer_calls, key=lambda call: call.time)

    def time(self):
        return str(self.time_sys)
   
    def day(self):
        return self.time_sys.day() 
