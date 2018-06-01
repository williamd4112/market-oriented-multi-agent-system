import logging
import os
import argparse
import numpy as np

from tabulate import tabulate

from simulator.city import City
from simulator.customer_call import CustomerCall

from auction.taxi_coordinator import TaxiCoordinator

from util.common import compute_route_distance

from config import Config

FORMAT = '[%(asctime)s %(filename)s:%(lineno)d] %(levelname)s: %(message)s'
SHIFTS = ['3AM-1PM', '9AM-7PM', '6PM-4AM']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--auction-type', help='Auction type of taxi coordinator', type=str, choices=['first-price', 'second-price'], required=True)
    parser.add_argument('--payment-rule', help='Payment computation rule', type=str, choices=['type-1', 'type-2', 'type-3'], required=True)
    parser.add_argument('--bidding-strategy', help='Bidding strategy of taxi drivers', type=str, choices=['truthful', 'lookahead'], default='truthful')
    parser.add_argument('--timelimit', help='Simulation timelimit (hour_simulation)', type=int, default=24)
    parser.add_argument('--waiting-time-threshold', help='Waiting time threshold (hour_simulation)', type=float, default=24)
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

    config = Config(waiting_time_threshold=args.waiting_time_threshold)
    city = City(config.intersections, initial_hour=0, lambd_schedule=config.city_lambd_schedule)
    coordinator = TaxiCoordinator(city=city, 
                auction_type=args.auction_type,
                payment_rule=args.payment_rule,
                bidding_strategy=args.bidding_strategy,
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
        if args.bidding_strategy == 'lookahead' and city.time_sys.hour_in_sim() % 8 == 0:
            coordinator.train()
            logging.info('Update the lookahead policy.')

    if args.dump_company_payoff:        
        coordinator.dump_history_payoff(os.path.join('data', 'company-history-payoff.npy'))

    # Print driver status
    print('===Drivers===')
    stats_drivers = []
    for driver in coordinator.drivers:        
        events = driver.generate_complete_schedule(args.timelimit).events
        distance_return = 0
        for e in events:
            if e.event_name == 'Return':
                distance_return += compute_route_distance(e.route)
        cost_return = distance_return * config.gas_cost_per_kilometer
        shift = SHIFTS[int(driver.idx // 4)]
        history_payoff_driver = driver.get_history_payoff()
        payoff_sum = history_payoff_driver.sum() - cost_return
        payoff_avg = payoff_sum / len(history_payoff_driver) if len(history_payoff_driver) > 0 else payoff_sum
        waiting_time_period_avg = driver.get_waiting_time_periods().mean()
        stats_drivers.append([shift, driver.idx, payoff_sum, payoff_avg, waiting_time_period_avg, cost_return])
        if args.dump:
            driver.generate_complete_schedule(args.timelimit, True).dump_json(os.path.join('data', 'driver-%03d.json' % (driver.idx)))
    print(tabulate(stats_drivers, 
            headers=['Shift', 'ID', 'Acc. payoff', 'Avg. payoff', 'Avg. waiting time (hours)', 'Return cost']))

    # Print company's status
    history_payoff = coordinator.get_history_payoff()
    all_waiting_time_periods = []
    for waiting_time_periods in [driver.get_waiting_time_periods() for driver in coordinator.drivers]:
        for t in waiting_time_periods:
            all_waiting_time_periods.append(t)
    all_waiting_time_periods = np.asarray(all_waiting_time_periods)
    stats_company = [[history_payoff.sum(), history_payoff.mean(), all_waiting_time_periods.mean()]]
    print('===Company===')
    print(tabulate(stats_company, 
            headers=['Acc. payoff', 'Avg. payoff', 'Avg. waiting time (hours)']))

 
