import logging
from simulator.city import City
from auction.taxi_coordinator import TaxiCoordinator

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logging.basicConfig(format=FORMAT)

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
                                    []],
                init_pos=(4, 8))
    print(coordinator.drivers)
    while city.day() < 1:
        customer_calls = city.step() 
        coordinator.allocate(customer_calls)
    
