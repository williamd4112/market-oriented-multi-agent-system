import logging
import os
import argparse

from simulator.city import City
from simulator.customer_call import CustomerCall

from auction.taxi_coordinator import TaxiCoordinator

from config import Config

FORMAT = '[%(asctime)s %(filename)s:%(lineno)d] %(levelname)s: %(message)s'
SHIFTS = ['3AM-1PM', '9AM-7PM', '6PM-4AM']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--auction-type', help='Auction type of taxi coordinator', type=str, choices=['first-price', 'second-price'], required=True)
    parser.add_argument('--timelimit', help='Simulation timelimit (hour_simulation)', type=int, default=24)
    parser.add_argument('--dump', help='Dump the drivers\' schedules to JSON', action='store_true', default=False)
    parser.add_argument('--dump-company-payoff', help='Dump the history payoff to npy', action='store_true', default=False)
    parser.add_argument('--verbose', help='Show log', type=str, choices=['info', 'debug'], default=None)
    args = parser.parse_args()
    
    level = logging.ERROR
    if args.verbose == 'info':
        level = logging.INFO
    elif args.verbose == 'debug':       
        level = logging.DEBUG

    logging.basicConfig(format=FORMAT, level=level, datefmt='%d-%m-%Y:%H:%M:%S')

    config = Config()
    city = City(config.intersections, initial_hour=0, lambd_schedule=config.city_lambd_schedule)
    coordinator = TaxiCoordinator(city=city, 
                auction_type=args.auction_type, 
                drivers_schedule=config.driver_schedules,
                init_pos=config.init_pos,
                payment_ratio=config.payment_ratio,
                driving_velocity=config.driving_velocity,
                charge_rate_per_kilometer=config.charge_rate_per_kilometer,
                gas_cost_per_kilometer=config.gas_cost_per_kilometer,
                waiting_time_threshold=config.waiting_time_threshold)

    while city.time_sys.hour_in_sim() < args.timelimit:
        customer_calls = city.step()
        coordinator.allocate(customer_calls)
    coordinator.dump_history_payoff(os.path.join('data', 'company-history-payoff.npy'))
    for driver in coordinator.drivers:
        '''
        events = driver.timeline.generate_complete_schedule(args.timelimit, True)
        for e in events:
            if e.event_name == 'Return':
        '''
        shift = SHIFTS[int(driver.idx // 4)]
        logging.info('Shift {} Driver-{} payoff {:.2f}, average customer waiting time period {:.2f} hours'.format(shift, driver.idx, driver.get_payoff(), driver.get_waiting_time_periods().mean()))
        if args.dump:
            driver.timeline.dump_json(os.path.join('data', 'driver-%03d.json' % (driver.idx)))
    logging.info('Company payoff: {:.2f}'.format(coordinator.get_payoff()))
 


