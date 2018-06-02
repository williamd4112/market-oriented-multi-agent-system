import json
import numpy as np

def compute_timings(start_time, route, speed):
    timings = [start_time]
    base_time = start_time
    prev_pos = route[0]
    for pos in route[1:]:
        offset = (abs(pos[0] - prev_pos[0]), abs(pos[1] - prev_pos[1]))        
        dist = sum(offset)
        elapsed_time = dist / speed
        timing = base_time + elapsed_time
        timings.append(timing)
    return timings

def compute(route, timings, t):            
    prev_pos, prev_timing = route[0], timings[0]
    for pos, timing in zip(route[1:], timings[1:]):
        if t >= prev_timing and t <= timing:
            ratio = (t - prev_timing) / (timing - prev_timing)            
            offset = (pos[0] - prev_pos[0], pos[1] - prev_pos[1])
            interp_pos = (prev_pos[0] + ratio * offset[0], prev_pos[1] + ratio * offset[1])
            return interp_pos
        prev_pos = pos
        prev_timing = timing
    return route[-1]
       
