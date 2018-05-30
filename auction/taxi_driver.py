import logging
import copy
import numpy as np

from sortedcontainers import SortedList

from util.timeline import TimeLine, TimeLineEvent


class Plan(object):
    def __init__(self, start_time, end_time, start_pos, pickup_pos, end_pos, waiting_time, pickup_distance, requested_distance, bid=0, route=None):
        self.start_time = start_time
        self.end_time = end_time
        self.start_pos = start_pos
        self.pickup_pos = pickup_pos
        self.end_pos = end_pos
        self.waiting_time = waiting_time
        self.pickup_distance = pickup_distance
        self.requested_distance = requested_distance
        self.bid = bid
        self.route = route

    def __repr__(self):
        return 'Plan(Time({}-{}), Waiting time: {}, Required time: {}, Pos({},{},{}), Pic Distance: {}, Req Distance:{}, Bid:{})'.format(self.start_time, self.end_time,
                                                                        (self.end_time - self.start_time),
                                                                        self.waiting_time,
                                                                        self.start_pos, self.pickup_pos, self.end_pos,
                                                                        self.pickup_distance,
                                                                        self.requested_distance,
                                                                        self.bid)

class TaxiDriver(object):
    def __init__(self, idx, init_pos, city_graph, bidding_strategy='truthful', 
            charge_rate_per_kilometer=60, gas_cost_per_kilometer=4, driving_velocity=30):
        self.idx = idx
        self.charge_rate_per_kilometer = charge_rate_per_kilometer
        self.gas_cost_per_kilometer = gas_cost_per_kilometer
        self.driving_velocity = driving_velocity
        self.current_payoff = 0
        self.bidding_strategy = bidding_strategy
        self.init_pos = init_pos
        self.city_graph = city_graph
        self.timeline = TimeLine()
        self.plans = SortedList(key=lambda plan: plan.start_time)

    def get_payoff(self):
        return self.current_payoff

    def get_waiting_times(self):
        return np.asarray([plan.waiting_time for plan in self.plans])

    def is_restricted(self, call):
        '''
        Check this driver is restriced
        '''
        # Get a latest call which this driver won
        plan = self._get_latest_plan()
        if plan is None: 
            return False

        # Compute restricted time period
        restricted_hrs = plan.requested_distance / self.driving_velocity
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
                time_period_to_origin = distance_to_origin / self.driving_velocity
                time_arrived_origin = plan.end_time + time_period_to_origin
                valid = (time_arrived_origin <= after_event.start_time)                
        return valid
       
    def assign(self, plan, payment_to_the_auction):
        '''
        Assign a plan for a driver. This call will be added to driver's schedule. The driver's payoff will be increased.
        '''    
        event = TimeLineEvent(plan.start_time, plan.end_time, 'Call', plan.route)
        self.timeline.add_event(event)
        self.plans.add(plan)
        
        plan_payoff = self._compute_payoff(distance_to_customer=plan.pickup_distance, distance_to_dest=plan.requested_distance, payment_to_the_auction=payment_to_the_auction)
        self.current_payoff += plan_payoff
        logging.debug('Driver-{} takes {}, payoff {}'.format(self.idx, plan, plan_payoff))

    def generate_plan(self, call):
        '''
        Generate a plan by call.
        '''
        return self._make_plan(call)

    def generate_complete_schedule(self, timelimit, use_relative_coordinate=False):
        '''
        For visualization:
        Fill the gap in the timeline with Free, Return, return a timeline object for visualization
        '''
        timeline_copy = copy.deepcopy(self.timeline)
        prev_e = None
        for e in self.timeline.events:
            if e.end_time <= timelimit:               
                if e.event_name == 'Call':
                    if prev_e is not None:
                        timeline_copy.add_event(TimeLineEvent(prev_e.end_time, e.start_time, 'Free'))
                if e.event_name == 'Shift':
                    if prev_e is not None and prev_e.event_name == 'Call':
                        # Compute time for return trip    
                        end_pos = prev_e.route[-1]
                        distance_end_pos_to_origin, route_end_pos_to_origin = self.city_graph.get_pos_shortest_distance(end_pos, self.init_pos)
                        time_period_end_pos_to_origin = distance_end_pos_to_origin / self.driving_velocity
                        time_start_return = e.start_time - time_period_end_pos_to_origin
                        # Verify return time is enough
                        if time_start_return < prev_e.end_time:
                            raise Exception('error: invalid event in the schedule')
                        # Add to timeline
                        timeline_copy.add_event(TimeLineEvent(time_start_return, e.start_time, 'Return', route_end_pos_to_origin))

                        # Fill the gap between call and return
                        if time_start_return > prev_e.end_time:
                            timeline_copy.add_event(TimeLineEvent(prev_e.end_time, time_start_return, 'Free'))
            prev_e = e
        # Fill the gap with free
        if prev_e is not None and prev_e.end_time < timelimit:
            timeline_copy.add_event(TimeLineEvent(prev_e.end_time, timelimit, 'Free'))

        # Tranform to relative coordinates
        if use_relative_coordinate:
            for e in timeline_copy.events:
                if e.event_name == 'Call' or e.event_name == 'Return':
                    orig_pos = e.route[0]
                    new_route = []
                    for idx, p in enumerate(e.route):
                        new_route.append((p[0] - orig_pos[0], p[1] - orig_pos[1]))
                        orig_pos = p
                    e.route = new_route
        return timeline_copy
 
    def _make_plan(self, call):
        before_event = self.timeline.get_before_event(call.time)

        # start_time = when to start to pickup + deliever the customer
        # if no plan: start from init_pos and start from calling time
        if len(self.plans) == 0:
            start_time = call.time
            start_pos = self.init_pos
        # if before event is Shift: start from init_pos
        elif before_event is not None and before_event.event_name == 'Shift':
            start_time = call.time
            start_pos = self.init_pos
        # otherwise: start from latest_plan's end pos and start from latest_plan's end time
        else:
            latest_plan = self._get_latest_plan()
            start_time = latest_plan.end_time if latest_plan.end_time > call.time else call.time
            start_pos = latest_plan.end_pos      
        pickup_pos = call.start_pos
        end_pos = call.destination_pos

        distance_to_customer, route_to_customer = self.city_graph.get_pos_shortest_distance(start_pos, pickup_pos)
        distance_to_dest, route_to_dest = self.city_graph.get_pos_shortest_distance(call.start_pos, call.destination_pos)
        route = route_to_customer + route_to_dest
        
        pickup_time = self._compute_waiting_time(distance_to_customer)

        # waiting_time = elapsed time from when call came to when the customer is pickuped
        waiting_time = call.time + pickup_time

        # driving_time = elapsed time from when the driver starts handling this call to when the customer arrived at the dest
        driving_time = self._compute_driving_time(distance_to_customer, distance_to_dest)

        end_time = start_time + driving_time
        
        bid = self._compute_bidding_price(distance_to_customer, distance_to_dest)

        plan = Plan(start_time, end_time, start_pos, pickup_pos, end_pos,
                waiting_time=waiting_time,
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

    def _compute_waiting_time(self, distance_to_customer):
        '''
        Retrive the waiting time for the customer
        '''
        return (distance_to_customer) / self.driving_velocity

    def _compute_driving_time(self, distance_to_customer, distance_to_dest):
        '''
        Retrive the required driving time from driver pos to customer's pos and customer's pos to dest
        '''
        return (distance_to_customer + distance_to_dest) / self.driving_velocity

    def _compute_bidding_price(self, distance_to_customer, distance_to_dest):
        '''
        Retrieve the bidding price.
        '''
        if self.bidding_strategy == 'truthful':
            # truthful bidding
            bid = self._compute_value(distance_to_customer, distance_to_dest)
        elif self.bidding_strategy == 'lookahead':
            # TODO: Implement lookahead bidding
            raise NotImplemented()
        return bid

    def _compute_value(self, distance_to_customer, distance_to_dest):
        '''
        Retrieve the true value of plan
        '''
        chargeable_distance = distance_to_dest
        charge_rate_per_kilometer = self.charge_rate_per_kilometer
        total_traveling_distance = (distance_to_customer + distance_to_dest)
        gas_cost_per_kilometer = self.gas_cost_per_kilometer
        return chargeable_distance * (charge_rate_per_kilometer) - total_traveling_distance * gas_cost_per_kilometer

    def _compute_payoff(self, distance_to_customer, distance_to_dest, payment_to_the_auction):
        '''
        Retrieve the driver payoff = 
            chargeable_distance * (charge_rate_per_kilometer) - total_traveling_distance * gas-cost-per-kilometer – payment_to_the_auction.
        '''   
        value = self._compute_value(distance_to_customer, distance_to_dest)
        return value - payment_to_the_auction
 
    def __repr__(self):
        return 'Driver({})'.format(str(self.timeline))
