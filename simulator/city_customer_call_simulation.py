import numpy as np
import random

from simulator.time_sys import TimeSystem
from simulator.customer_call import CustomerCall
from util.distribution import NormalDistribution, PoissonProcess

class CityCustomerCallSimulation(object):
    def __init__(self, intersections, city_graph, time_sys):
        self.intersections = intersections
        self.city_graph = city_graph
        self.time_sys = time_sys

        self.poisson_process = PoissonProcess()
        self.normal_distribution = NormalDistribution(mu=2.0, sigma=1.5)

    def set(self, lambd):
        self.poisson_process.set(lambd)

    def __call__(self):
        customer_calls = []
        for intersection in self.intersections:
            customer_calls += self._generate_customer_calls_at_intersection(intersection)
        return customer_calls
                      
    def _generate_customer_calls_at_intersection(self, intersection):
        start_node_idx = self.city_graph.get_id(intersection)
        accumulated_time = 0
        customer_calls = []
        while True:
            next_call_elapsed_time = self.poisson_process()
            time = self.time_sys.hour_in_sim() + accumulated_time + next_call_elapsed_time 
            travelling_distance = self.normal_distribution()
            if travelling_distance <= 0:
                raise Exception('Error: travelling distance must be larger than zero, distance = %f' % (travelling_distance))
            possible_destinations = self.city_graph.get_poses_on_distance(start_node_idx, travelling_distance)
            sampled_destination = random.choice(possible_destinations)            
            customer_call = CustomerCall(intersection, sampled_destination, travelling_distance, time)
            customer_calls.append(customer_call)
            accumulated_time += next_call_elapsed_time
            
            if accumulated_time >= 1:
                break
        return customer_calls

