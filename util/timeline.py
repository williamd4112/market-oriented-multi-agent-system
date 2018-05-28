from sortedcontainers import SortedList
from collections import namedtuple

TimeLineEvent = namedtuple('TimeLineEvent', ['start_time', 'end_time', 'event_name'])
Endpoint = namedtuple('Endpoint', ['time', 'type'])

TYPE_START = True
TYPE_END = False

def _is_overlap(e1, e2):
    '''
    Assume e1, e2 are TimeLineEvent and their start_time < end_time
    '''
    if e1.start_time == e2.start_time:
        return True
    elif e1.start_time < e2.start_time:
        return e1.end_time > e2.start_time
    elif e1.start_time > e2.start_time:
        return e2.end_time > e1.start_time

class TimeLine(object):
    def __init__(self):
        self.events = SortedList(key=lambda e: e.start_time)
    
    def add_event(self, e):
        valid = self.is_valid(e)
        if valid:
            self.events.add(e)
        return valid

    def is_valid(self, e):
        if e.start_time >= e.end_time:
            raise Exception('Error: start time > end_time.')
        if len(self.events) == 0:
            return True
        else:
            for existing_event in self.events:
                if existing_event.start_time > e.end_time:
                    return True
                if _is_overlap(e, existing_event):
                    return False
            return True

    def __repr__(self):
        event_reprs = []
        for e in self.events:
            event_reprs.append("({}: {} - {})".format(e.event_name, e.start_time, e.end_time))        
        return ','.join(event_reprs)
        

