import logging
import os
import argparse

from simulator.city import City
from simulator.customer_call import CustomerCall

from auction.taxi_coordinator import TaxiCoordinator

from config import Config

FORMAT = '[%(asctime)s %(pathname)s:%(lineno)d] %(levelname)s: %(message)s'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--auction-type', help='Auction type of taxi coordinator', type=str, choices=['first-price', 'second-price'], required=True)
    parser.add_argument('--timelimit', help='Simulation timelimit (hour_simulation)', type=int, default=24)
    parser.add_argument('--dump', help='Dump the drivers\' schedules to JSON', action='store_true', default=False)
    args = parser.parse_args()

    logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt='%d-%m-%Y:%H:%M:%S')

    config = Config()
    city = City(config.intersections, initial_hour=0, lambd_schedule=config.city_lambd_schedule)
    coordinator = TaxiCoordinator(city=city, 
                auction_type=args.auction_type, 
                drivers_schedule=config.driver_schedules,
                init_pos=config.init_pos)
    while city.time_sys.hour_in_sim() < args.timelimit:
        customer_calls = city.step() 
        coordinator.allocate(customer_calls)
    for driver in coordinator.drivers:
        logging.info('Driver-{} payoff {}'.format(driver.idx, driver.get_payoff()))
        if args.dump:
            driver.timeline.dump_json(os.path.join('data', 'driver-%03d.json' % (driver.idx)))
    logging.info('Company payoff: {}'.format(coordinator.get_payoff()))
 

