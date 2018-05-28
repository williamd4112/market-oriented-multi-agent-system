import logging
import numpy as np

from sortedcontainers import SortedList

from util.timeline import TimeLine, TimeLineEvent

VELOCITY = 30

class Plan(object):
    def __init__(self, start_time, end_time, start_pos, end_pos, pickup_distance, requested_distance, bid=0, route=None):
        self.start_time = start_time
        self.end_time = end_time
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.pickup_distance = pickup_distance
        self.requested_distance = requested_distance
        self.bid = bid
        self.route = route

    def __repr__(self):
        return 'Plan(Time({} - {}), Required time: {}, Pos({}, {}), Pic Distance: {}, Req Distance:{}, Bid:{})'.format(self.start_time, self.end_time,
                                                                        (self.end_time - self.start_time),
                                                                        self.start_pos, self.end_pos,
                                                                        self.pickup_distance,
                                                                        self.requested_distance,
                                                                        self.bid)

class TaxiDriver(object):
    def __init__(self, idx, init_pos, city_graph):
        self.idx = idx
        self.payoff = 0
        self.init_pos = init_pos
        self.city_graph = city_graph
        self.timeline = TimeLine()
        self.plans = SortedList(key=lambda plan: plan.start_time)

    def is_restricted(self, call):
        '''
        Check this driver is restriced
        '''
        # Get a latest call which this driver won
        plan = self._get_latest_plan()
        if plan is None: 
            return False

        # Compute restricted time period
        restricted_hrs = plan.requested_distance / VELOCITY
        # Compute forbidden time
        latest_start_time = plan.start_time
        forbidden_time = latest_start_time + restricted_hrs
        
        return call.time < forbidden_time

    def is_available(self, plan):
        '''
        Check availability of this driver based on timeline.
        '''
        event = TimeLineEvent(plan.start_time, plan.end_time, 'Call')
        # Check overlap
        valid = self.timeline.is_valid(event)
        # Check return trip
        after_event = self.timeline.get_after_event(event.start_time)
        if after_event is not None:
            if after_event.event_name == 'Shift':
                dest = plan.end_pos
                distance_to_origin, _ = self.city_graph.get_pos_shortest_distance(dest, self.init_pos)
                time_period_to_origin = distance_to_origin / VELOCITY
                time_arrived_origin = plan.end_time + time_period_to_origin
                valid = (time_arrived_origin <= after_event.start_time)                
        return valid
       
    def assign(self, plan):
        '''
        Assign a plan for a driver. This call will be added to driver's schedule. The driver's payoff will be increased.
        '''    
        event = TimeLineEvent(plan.start_time, plan.end_time, 'Call', plan.route)
        self.timeline.add_event(event)
        self.plans.add(plan)
        
        # TODO: Compute payoff
        print('Driver-{} takes {}'.format(self.idx, plan))

    def generate_plan(self, call):
        '''
        Generate a plan by call.
        '''
        return self._make_plan(call)
    
    def _make_plan(self, call):

        # if no plan: start from init_pos and start from calling time
        if len(self.plans) == 0:
            start_time = call.time
            start_pos = self.init_pos
        # otherwise: start from latest_plan's end pos and start from latest_plan's end time
        else:
            latest_plan = self._get_latest_plan()
            start_time = latest_plan.end_time
            start_pos = latest_plan.end_pos      
       
        end_pos = call.destination_pos

        distance_to_customer, route_to_customer = self.city_graph.get_pos_shortest_distance(start_pos, end_pos)
        distance_to_dest, route_to_dest = self.city_graph.get_pos_shortest_distance(call.start_pos, call.destination_pos)
        route = route_to_customer + route_to_dest

        driving_time = self._compute_driving_time(distance_to_customer, distance_to_dest)
        end_time = start_time + driving_time
        
        bid = self._compute_bidding_price(distance_to_customer, distance_to_dest)

        plan = Plan(start_time, end_time, start_pos, end_pos,
                pickup_distance=distance_to_customer,
                requested_distance=distance_to_dest,
                bid=bid,
                route=route)

        return plan

    def _get_latest_plan(self):
        '''
        Retrieve the latest plan from plans
        '''
        if len(self.plans) == 0: 
            return None
        return self.plans[-1]

    def _compute_driving_time(self, distance_to_customer, distance_to_dest):
        '''
        Retrive the required driving time from driver pos to customer's pos and customer's pos to dest
        '''
        return (distance_to_customer + distance_to_dest) / VELOCITY

    def _compute_bidding_price(self, distance_to_customer, distance_to_dest):
        '''
        Retrieve the bidding price.
        '''
        # TODO: Return bidding price with bidding strategy
        return 1
    
    def __repr__(self):
        return 'Driver({})'.format(str(self.timeline))
