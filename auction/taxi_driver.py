import logging
import numpy as np

from sortedcontainers import SortedList

from util.timeline import TimeLine, TimeLineEvent

VELOCITY = 30

class Plan(object):
    def __init__(self, start_time, end_time, start_pos, end_pos, requested_distance, bid=0):
        self.start_time = start_time
        self.end_time = end_time
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.requested_distance = requested_distance
        self.bid = bid

    def __repr__(self):
        return 'Plan(Time({} - {}), Required time: {}, Pos({}, {}), Distance:{}, Bid:{})'.format(self.start_time, self.end_time,
                                                                        (self.end_time - self.start_time),
                                                                        self.start_pos, self.end_pos,
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
        Check availability of this driver
        '''
        event = TimeLineEvent(plan.start_time, plan.end_time, 'Call')
        valid = self.timeline.is_valid(event) 
        #print('Event', event, 'Valid', valid)
        return valid
       
    def assign(self, plan):
        '''
        Assign a plan for a driver. This call will be added to driver's schedule. The driver's payoff will be increased.
        '''    
        event = TimeLineEvent(plan.start_time, plan.end_time, 'Call')
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
        driving_time = self._compute_driving_time(start_pos, call)
        end_time = start_time + driving_time
        end_pos = call.destination_pos
        
        # TODO: accumulated payoff
        # TODO: compute route
        # TODO: compute bidding price

        plan = Plan(start_time, end_time, start_pos, end_pos, requested_distance=call.distance)

        return plan

    def _get_latest_plan(self):
        '''
        Retrieve the latest plan from plans
        '''
        if len(self.plans) == 0: 
            return None
        return self.plans[-1]

    def _compute_driving_time(self, start_pos, call):
        '''
        Retrive the required driving time from driver pos to customer's pos and customer's pos to dest
        '''
        # TODO: Compute driver to customer pos
        return call.distance / VELOCITY
    
    def __repr__(self):
        return 'Driver({})'.format(str(self.timeline))
