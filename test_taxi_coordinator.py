import logging
import os
import argparse

from simulator.city import City
from simulator.customer_call import CustomerCall
from auction.taxi_coordinator import TaxiCoordinator

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def test_allocate():
    intersections = [ 
	    # (x,y) is the place of a intersection
        (0,0), (0,2), (0,6), (0,8), (0,12), (0,14),
        (2,0), (2,2), (2,6), (2,7), (2,8) , (2,12), (2,14),
        (3,0), (3,2), (3,6), (3,7), (3,8) , (3,12), (3,14),
        (4,0), (4,2), (4,4), (4,6), (4,7) , (4,8) , (4,12), (4,14),
        (5,0), (5,2), (5,4), (5,6), (5,8) , (5,12), (5,14),
        (7,0), (7,2), (7,4), (7,6), (7,8) , (7,12), (7,14),
    ]
    city = City(intersections, 0, None)
    coordinator = TaxiCoordinator(city=city, 
                auction_type='first-price', 
                drivers_schedule=[  #[(0, 12)],
                                    #[(0, 12)],
                                    [10, 24]],
                init_pos=(4, 8))
    print(coordinator.drivers)
    while city.time_sys.hour_in_sim() < 24:
        customer_calls = city.step() 
        coordinator.allocate(customer_calls)

def test_start_from_shift():
    intersections = [ 
	    # (x,y) is the place of a intersection
        (0,0), (0,2), (0,6), (0,8), (0,12), (0,14),
        (2,0), (2,2), (2,6), (2,7), (2,8) , (2,12), (2,14),
        (3,0), (3,2), (3,6), (3,7), (3,8) , (3,12), (3,14),
        (4,0), (4,2), (4,4), (4,6), (4,7) , (4,8) , (4,12), (4,14),
        (5,0), (5,2), (5,4), (5,6), (5,8) , (5,12), (5,14),
        (7,0), (7,2), (7,4), (7,6), (7,8) , (7,12), (7,14),
    ]
    city = City(intersections, 0, None)
    coordinator = TaxiCoordinator(city=city, 
                auction_type='second-price', 
                drivers_schedule=[  #[(0, 12)],
                                    #[(0, 12)],
                                    [(5, 10)]],
                init_pos=(4, 8))
    print(coordinator.drivers)
    customer_calls = [  CustomerCall((4, 4), (5, 4), 1),
                        CustomerCall((5, 6), (5, 8), 2),
                        CustomerCall((4, 7), (4, 12), 11)]
    coordinator.allocate(customer_calls)
    schedule = coordinator.drivers[0].generate_complete_schedule(16, True)
    print('Schedule')
    for e in schedule.events:
        print(e)

def test_payoff_bidding():
    intersections = [ 
	    # (x,y) is the place of a intersection
        (0,0), (0,2), (0,6), (0,8), (0,12), (0,14),
        (2,0), (2,2), (2,6), (2,7), (2,8) , (2,12), (2,14),
        (3,0), (3,2), (3,6), (3,7), (3,8) , (3,12), (3,14),
        (4,0), (4,2), (4,4), (4,6), (4,7) , (4,8) , (4,12), (4,14),
        (5,0), (5,2), (5,4), (5,6), (5,8) , (5,12), (5,14),
        (7,0), (7,2), (7,4), (7,6), (7,8) , (7,12), (7,14),
    ]
    city = City(intersections, 0, None)
    coordinator = TaxiCoordinator(city=city, 
                auction_type='second-price', 
                drivers_schedule=[  [],
                                    [],
                                    []],
                init_pos=(4, 8))
    while city.time_sys.hour_in_sim() < 24*7:
        customer_calls = city.step() 
        coordinator.allocate(customer_calls)
    for driver in coordinator.drivers:
        print('Driver-{} payoff {}'.format(driver.idx, driver.get_payoff()))
    print('Company payoff', coordinator.get_payoff())

def test_dump_json():
    intersections = [ 
	    # (x,y) is the place of a intersection
        (0,0), (0,2), (0,6), (0,8), (0,12), (0,14),
        (2,0), (2,2), (2,6), (2,7), (2,8) , (2,12), (2,14),
        (3,0), (3,2), (3,6), (3,7), (3,8) , (3,12), (3,14),
        (4,0), (4,2), (4,4), (4,6), (4,7) , (4,8) , (4,12), (4,14),
        (5,0), (5,2), (5,4), (5,6), (5,8) , (5,12), (5,14),
        (7,0), (7,2), (7,4), (7,6), (7,8) , (7,12), (7,14),
    ]
    city = City(intersections, 0, None)
    coordinator = TaxiCoordinator(city=city, 
                auction_type='second-price', 
                drivers_schedule=[  #[(0, 12)],
                                    #[(0, 12)],
                                    [(5, 10)]],
                init_pos=(4, 8))
    print(coordinator.drivers)
    customer_calls = [  CustomerCall((4, 4), (5, 4), 1),
                        CustomerCall((5, 6), (5, 8), 2),
                        CustomerCall((4, 7), (4, 12), 11)]
    coordinator.allocate(customer_calls)
    schedule = coordinator.drivers[0].generate_complete_schedule(16, True)
    print('Schedule')
    for e in schedule.events:
        print(e)
    schedule.dump_json(os.path.join('data', 'driver_0.json'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--case', type=str, required=True)
    args = parser.parse_args()
    
    if args.case == 'payoff_bidding':
        test_payoff_bidding()
    elif args.case == 'shift':
        test_start_from_shift()
    elif args.case == 'dump_json':
        test_dump_json()
