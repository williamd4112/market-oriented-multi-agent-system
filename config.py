import copy

from util.common import daily_schedules_to_weekly_schedules

class Config(object):
    def __init__(self, payment_ratio=0.3, waiting_time_threshold=1./12.):
        self.intersections = [ 
            (0,0), (0,2), (0,6), (0,8), (0,12), (0,14),
            (2,0), (2,2), (2,6), (2,7), (2,8) , (2,12), (2,14),
            (3,0), (3,2), (3,6), (3,7), (3,8) , (3,12), (3,14),
            (4,0), (4,2), (4,4), (4,6), (4,7) , (4,8) , (4,12), (4,14),
            (5,0), (5,2), (5,4), (5,6), (5,8) , (5,12), (5,14),
            (7,0), (7,2), (7,4), (7,6), (7,8) , (7,12), (7,14),
        ]
        self.init_pos = (4, 8)

        # schedule of city lambda value
        self.city_lambd_schedule = [(7, 9, 3.0), (17, 19, 3.0), (9, 17, 2.0), (19, 23, 2.0)]

        # schedule of drivers
        self.driver_schedules = []
        schedule_3am_1pm = [(3, 13)]
        schedule_9am_7pm = [(9, 19)]
        schedule_6pm_4am = [(18, 28)]
        self.driver_schedules += ([copy.copy(schedule_3am_1pm) for _ in range(4)])
        self.driver_schedules += ([copy.copy(schedule_9am_7pm) for _ in range(4)])
        self.driver_schedules += ([copy.copy(schedule_6pm_4am) for _ in range(4)])
        self.driver_schedules = daily_schedules_to_weekly_schedules(self.driver_schedules)

        # hyperparameters for payoff computation
        self.payment_ratio = payment_ratio
        self.charge_rate_per_kilometer = 60
        self.gas_cost_per_kilometer = 4
        self.driving_velocity = 30
        self.waiting_time_threshold = waiting_time_threshold




