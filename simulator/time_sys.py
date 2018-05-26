import numpy as np

class TimeSystem(object):
    '''
    A time system use hour as atomic unit.
    '''
    PERIOD = 24
    HALF_PERIOD = PERIOD / 2
    PERIOD_REPRS = ['AM', 'PM']
    
    def __init__(self, initial_hour):
        self.current_hour = initial_hour
    
    def step(self, stride=1):
        self.current_hour += stride
        self.current_hour %= TimeSystem.PERIOD

    def __call__(self):
        return self.current_hour
    
    def __repr__(self):
        hour = int(self.current_hour % TimeSystem.HALF_PERIOD)
        rep = int(self.current_hour / TimeSystem.HALF_PERIOD)        
        return '%d%s' % (hour, TimeSystem.PERIOD_REPRS[rep])


if __name__ == '__main__':
    sys = TimeSystem(12)
    print(sys)

    
