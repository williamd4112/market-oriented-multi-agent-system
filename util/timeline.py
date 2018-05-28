import json

from sortedcontainers import SortedList
from collections import namedtuple

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

class TimeLineEvent(object):
    def __init__(self, start_time, end_time, event_name=None, route=None):
        self.start_time = start_time
        self.end_time = end_time
        self.event_name = event_name
        self.route = route

    def __jsonencode__(self):
        return self.__dict__

class TimeLineEventJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TimeLineEvent):
            return obj.__jsonencode__()
        return json.JSONEncoder.default(self, obj)

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

    def get_event(self, time):
        for e in self.events:
            if time >= e.start_time and time <= e.end_time:
                return e
        return None

    def get_after_event(self, time):
        for e in self.events:
            if e.start_time > time:
                return e
        return None

    def __repr__(self):
        event_reprs = []
        for e in self.events:
            event_reprs.append("({}: {} - {})".format(e.event_name, e.start_time, e.end_time))        
        return ','.join(event_reprs)

    def dump_json(self, path):
        l = [e for e in self.events]
        with open(path, 'w') as f:
            json.dump(l, f, cls=TimeLineEventJSONEncoder)


        

