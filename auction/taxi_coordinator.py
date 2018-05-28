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
            # Find all unrestricted drivers, if there is no unrestricted drivers, drop this call
            unrestricted_drivers = self._get_unrestricted_drivers(customer_call)
            if len(unrestricted_drivers) > 0:
                # Request drivers's plans
                plans = [driver.generate_plan(customer_call) for driver in unrestricted_drivers]

                # Check the availability with drivers' timeline
                available_drivers_and_plans = [(driver, plan) for driver, plan in zip(unrestricted_drivers, plans) if driver.is_available(plan)]

                print(available_drivers_and_plans)
                # Send this call to all drivers
                #bids = [driver.bid(customer_call) for driver in available_drivers]

                # Select the drivers according to auction algorithm
                #winner_index = self._choose_bid(bids)
                
                # Assign the customer call to the winner
                #available_drivers[winner_index].assign(customer_call)
                
                # Increase the coordinator's payoff
                #self._deal_call(customer_call)

    def _init_drivers(self, drivers_schedule):
        '''
        Initialize all drivers by schedules.
        Each schedule is a tuple (shift_start, shift_end) in simulation time(hr)
        '''        
        drivers = []
        for schedule in drivers_schedule:
            driver = TaxiDriver(init_pos=self.init_pos, city_graph=self.city.city_graph)
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

    def _choose_bid(self, bids):
        '''
        Select a bidder according to the set auction type.
        '''
        raise NotImplemented()

    def _deal_call(self, call):
        '''
        Increase the coordinator's payoff with this call.
        '''        
        raise NotImplemented()
