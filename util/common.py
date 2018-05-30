import numpy as np

def check_duplicated_element(l):
    return len(l) != len(set(l))

def movement_to_dir(mov):
    direction = (np.sign(mov[0]), np.sign(mov[1]))
    return direction

def daily_schedules_to_weekly_schedules(daily_schedule_for_drivers):
    '''
    Pass the daily schedules, convert to weekly schedule for each drivers.
    '''
    weekly_schedules_for_drivers = []

    print(daily_schedule_for_drivers)
    for daily_schedule_for_driver in daily_schedule_for_drivers:
        weekly_schedules_for_driver = []
        for start_time, end_time in daily_schedule_for_driver:
            for day in range(7):
                weekly_schedules_for_driver.append((24 * day + start_time, 24 * day + end_time))
        weekly_schedules_for_drivers.append(weekly_schedules_for_driver)
    return weekly_schedules_for_drivers
        
        
