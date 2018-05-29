import numpy as np

from auction.taxi_driver import TaxiDriver
from util.timeline import TimeLineEvent

class TaxiCoordinator(object):
    def __init__(self, city, auction_type, drivers_schedule, init_pos):
        '''
        city: where the taxi coordinator works on
        auction_type: auction mechanism
        drivers_schedule: determine how many drivers in a period.
        init_pos: initial pos of all drivers
        '''
        self.city = city 
        self.auction_type = auction_type
        self.init_pos = init_pos
        self.drivers = self._init_drivers(drivers_schedule)
        self.current_payoff = 0

    def allocate(self, customer_calls):    
        # TODO: Consider look-ahead (consider multiple calls at a time)
        for customer_call in customer_calls:
            has_call_taken = False
            # Find all unrestricted drivers, if there is no unrestricted drivers, drop this call
            unrestricted_drivers = self._get_unrestricted_drivers(customer_call)
            if len(unrestricted_drivers) > 0:
                # Request drivers's plans
                plans = [driver.generate_plan(customer_call) for driver in unrestricted_drivers]

                # Check the availability with drivers' timeline
                available_drivers_and_plans = [(driver, plan) for driver, plan in zip(unrestricted_drivers, plans) if driver.is_available(plan)]                                               
                # TODO: Check if the drivers want to give up this call

                if len(available_drivers_and_plans) > 0:
                    # Select the drivers according to auction algorithm
                    winner_driver, winner_plan, winner_payment = self._choose_bid(available_drivers_and_plans)
                    
                    # Assign the customer call to the winner
                    winner_driver.assign(winner_plan, winner_payment)
                    
                    # Increase the coordinator's payoff
                    self._deal_call(customer_call)
                    has_call_taken = True
            if has_call_taken:
                print('Accept {}'.format(customer_call))

    def _init_drivers(self, drivers_schedule):
        '''
        Initialize all drivers by schedules.
        Each schedule is a tuple (shift_start, shift_end) in simulation time(hr)
        '''        
        drivers = []
        for idx, schedule in enumerate(drivers_schedule):
            driver = TaxiDriver(idx=idx, init_pos=self.init_pos, city_graph=self.city.city_graph)
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
        
        # TODO: Remove when done
        for driver_plan in sorted_drivers_and_plans:
            print('Driver-{} bid {}'.format(driver_plan[0].idx, driver_plan[1].bid))
        
        payment_ratio = 0.3
        charge_rate_per_kilometer = 60
        gas_cost_per_kilometer = 4
        
        driver = sorted_drivers_and_plans[0][0]
        plan = sorted_drivers_and_plans[0][1]

        if self.auction_type == 'first-price':
            bid = sorted_drivers_and_plans[0][1].bid
            payment = payment_ratio * (charge_rate_per_kilometer - gas_cost_per_kilometer) * plan.requested_distance - bid
            return driver, plan, payment
        elif self.auction_type == 'second-price':
            bid = sorted_drivers_and_plans[1][1].bid
            payment = payment_ratio * (charge_rate_per_kilometer - gas_cost_per_kilometer) * plan.requested_distance - bid
            return driver, plan, payment
        else:
            raise Exception('error: invalid auction_type.')
     
    def _deal_call(self, plan):
        '''
        Increase the coordinator's payoff with this plan.
        '''        
        # TODO: Compute pay-off
        self.current_payoff = 0 
