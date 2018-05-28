import numpy as np

from sortedcontainers import SortedList

from util.timeline import TimeLine, TimeLineEvent

VELOCITY = 30

class Plan(object):
    def __init__(self, start_time, end_time, start_pos, end_pos, requested_distance):
        self.start_time = start_time
        self.end_time = end_time
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.requested_distance = requested_distance

class TaxiDriver(object):
    def __init__(self, init_pos, city_graph):
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
        # Compute restricted time period
        restricted_hrs = plan.distance / VELOCITY
        # Compute forbidden time
        latest_start_time = plan.start_time
        forbidden_time = latest_start_time + restricted_hrs
        
        return call.time < forbidden_time

    def is_available(self, plan):
        '''
        Check availability of this driver
        '''
        plan = self._make_plan(call)
        event = TimeLineEvent(plan.start_time, plan.end_time, 'Call')
        return self.timeline.is_valid(event) 
       
    def bid(self, plan):
        '''
        Return a bidding price according to the bidding strategy
        '''
        raise NotImplemented()

    def assign(self, call):
        '''
        Assign a call for a driver. This call will be added to driver's schedule. The driver's payoff will be increased.
        '''    
        raise NotImplemented()

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
        Retrive the required driving time from driver pos to dest.
        '''
        raise NotImplemented()
    
    def __repr__(self):
        return 'Driver({})'.format(str(self.timeline))
