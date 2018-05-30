import logging
import numpy as np

from auction.taxi_driver import TaxiDriver
from util.timeline import TimeLineEvent

class TaxiCoordinator(object):
    def __init__(self, city, auction_type, drivers_schedule, init_pos, driving_velocity=30,
                    payment_ratio=0.3, charge_rate_per_kilometer=60, gas_cost_per_kilometer=4, waiting_time_threshold=15):
        '''
        city: where the taxi coordinator works on
        auction_type: auction mechanism
        drivers_schedule: determine how many drivers in a period.
        init_pos: initial pos of all drivers
        '''
        self.driving_velocity = driving_velocity
        self.payment_ratio = payment_ratio
        self.charge_rate_per_kilometer = charge_rate_per_kilometer
        self.gas_cost_per_kilometer = gas_cost_per_kilometer
        self.waiting_time_threshold = waiting_time_threshold
        self.city = city 
        self.auction_type = auction_type
        self.init_pos = init_pos
        self.drivers = self._init_drivers(drivers_schedule)
        self.current_payoff = 0
        self.history_payoff = []
        self.prev_time = 0

    def get_payoff(self):
        '''
        Retrieve the payoff (DO NOT DIRECTLY ACCESS CURRENT_PAYOFF. ACCESS CURRENT_PAYOFF WITH THIS FUNCTION.)
        '''
        return self.current_payoff

    def dump_history_payoff(self, path):
        np.save(path, np.asarray(self.history_payoff))

    def allocate(self, customer_calls):        
        for customer_call in customer_calls:
            if self.prev_time > customer_call.time:            
                raise Exception('error: customer_calls must be sorted. ({} > {})'.format(self.prev_time, customer_call.time))
            self.prev_time = max(customer_call.time, self.prev_time)
            has_call_taken = False
            # Find all unrestricted drivers, if there is no unrestricted drivers, drop this call
            unrestricted_drivers = self._get_unrestricted_drivers(customer_call)
            if len(unrestricted_drivers) > 0:
                # Request drivers's plans
                plans = [driver.generate_plan(customer_call) for driver in unrestricted_drivers]

                # Check the availability with drivers' timeline
                available_drivers_and_plans = [(driver, plan) for driver, plan in zip(unrestricted_drivers, plans) if driver.is_available(plan) and plan.waiting_time_period < self.waiting_time_threshold]                 
                # TODO: Check if the drivers want to give up this call

                if len(available_drivers_and_plans) > 0:
                    # Select the drivers according to auction algorithm
                    winner_driver, winner_plan, winner_payment = self._choose_bid(available_drivers_and_plans)
                    
                    # Assign the customer call to the winner
                    winner_driver.assign(winner_plan, winner_payment)
                    
                    # Increase the coordinator's payoff
                    self._accumulate_payoff(winner_payment)
                    self.history_payoff.append(winner_payment)
                    has_call_taken = True
            if has_call_taken:
                logging.debug('Accept {}'.format(customer_call))
            else:                
                logging.debug('Reject {}'.format(customer_call))

    def _init_drivers(self, drivers_schedule):
        '''
        Initialize all drivers by schedules.
        Each schedule is a tuple (shift_start, shift_end) in simulation time(hr)
        '''        
        drivers = []
        for idx, schedule in enumerate(drivers_schedule):
            driver = TaxiDriver(idx=idx, init_pos=self.init_pos, city_graph=self.city.city_graph,
                            charge_rate_per_kilometer=self.charge_rate_per_kilometer,
                            gas_cost_per_kilometer=self.gas_cost_per_kilometer,
                            driving_velocity=self.driving_velocity)
            for event in schedule:
                driver.timeline.add_event(TimeLineEvent(event[0], event[1], 'Shift')) 
            drivers.append(driver)
        return drivers

    def _get_unrestricted_drivers(self, customer_call):
        '''
        Retrieve all unrestricted drivers according to the availability rule.
        '''
        unrestricted_drivers = []
        
        for driver in self.drivers:
            if not driver.is_restricted(customer_call):            
                unrestricted_drivers.append(driver)
        return unrestricted_drivers

    def _choose_bid(self, drivers_and_plans):
        '''
        Select a driver according to its bidding price in the plan.
        Return a winner driver and a winner payment:
            winning_payment = 30% * (charge_rate_per_kilometer - gas_cost_per_kilometer)* requested_distance – {lowest bidding-price or second lowest bidding price}
        '''
        assert len(drivers_and_plans) > 0
        if len(drivers_and_plans) == 1:
            return drivers_and_plans[0][0], drivers_and_plans[0][1], drivers_and_plans[0][1].bid
        sorted_drivers_and_plans = sorted(drivers_and_plans, key=lambda dp: dp[1].bid)
               
        payment_ratio = self.payment_ratio
        charge_rate_per_kilometer = self.charge_rate_per_kilometer
        gas_cost_per_kilometer = self.gas_cost_per_kilometer
        
        driver = sorted_drivers_and_plans[0][0]
        plan = sorted_drivers_and_plans[0][1]

        if self.auction_type == 'first-price':
            bid = sorted_drivers_and_plans[0][1].bid
        elif self.auction_type == 'second-price':
            bid = sorted_drivers_and_plans[1][1].bid
        else:
            raise Exception('error: invalid auction_type.')
        # TODO: I think '+' is more correct than '-' in bid?
        payment = payment_ratio * (charge_rate_per_kilometer - gas_cost_per_kilometer) * plan.requested_distance - bid
        return driver, plan, payment
     
    def _accumulate_payoff(self, payment):
        '''
        Increase the coordinator's payoff with payment
        '''
        self.current_payoff += payment
