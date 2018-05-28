import numpy as np
import math

class TimeSystem(object):
    '''
    A time system use hour as atomic unit.
    '''
    PERIOD = 24
    HALF_PERIOD = PERIOD / 2
    PERIOD_REPRS = ['AM', 'PM']
    
    def __init__(self, initial_hour, initial_day=0):
        self.current_sim_hour = initial_hour * initial_day + initial_hour
    
    def step(self, stride=1):
        self.current_sim_hour += stride
        self.current_day = math.floor(self.current_sim_hour / TimeSystem.PERIOD)          
        self.current_hour = self.current_sim_hour % TimeSystem.PERIOD

    def day(self):
        return math.floor(self.hour_in_sim() / TimeSystem.PERIOD)          

    def hour_in_half_day(self):
        return self.hour_in_a_day() % TimeSystem.HALF_PERIOD

    def hour_in_a_day(self):
        return self.hour_in_sim() % TimeSystem.PERIOD
    
    def hour_in_sim(self):
        return self.current_sim_hour
 
    def __repr__(self):
        day = self.day()
        hour = int(self.hour_in_half_day())
        rep = int(self.hour_in_a_day() / TimeSystem.HALF_PERIOD)        
        return '%dd%dh%s' % (day, hour, TimeSystem.PERIOD_REPRS[rep])

if __name__ == '__main__':
    sys = TimeSystem(12)
    print(sys)

    
