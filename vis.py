import pygame
import sys
import json
import os
from gen_vis import compute_timings, compute

SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
CIRCLE_RADIUS = 30

# Initialization
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Circles')
fps = pygame.time.Clock()
paused = False

class Car(object):
    def __init__(self, schedule, speed):
        self.schedule = schedule
        self.speed = speed
        self.pos = [4, 8]
        self.prev_event = None    
    
    def update(self, t):
        print('time', t)
        for s in self.schedule:   
            if t >= s['start_time'] and t < s['end_time']:
                event_name = s['event_name']
                print('event', event_name)
                if event_name == 'Free':
                    if self.prev_event is None:
                        self.pos = [4, 8]
                    elif self.prev_event['event_name'] == 'Call' or self.prev_event['event_name'] == 'Return':
                        self.pos = self.prev_event['route'][-1]
                if event_name == 'Call' or event_name == 'Return':                            
                    timings = compute_timings(s['start_time'], s['route'], self.speed)
                    print(timings)
                    self.pos = compute(s['route'], timings, t)
                if event_name == 'Shift': self.pos = [4, 8]
                self.prev_event = s                
                break
    def draw(self):        
        global screen
        pos = [int(self.pos[0] * 20 + 320), int(self.pos[1] * 20 + 320)]
        print(pos, self.pos)
        pygame.draw.circle(screen, RED, pos, CIRCLE_RADIUS, 0)

path = os.path.join('data', 'driver-relative-0-000.json')
with open(path, 'r') as f:
    schedule = json.load(f)
cars = [Car(schedule, 30)]

def update(t):
    for car in cars:
        car.update(t)    

def render():
    screen.fill(BLACK)
    for car in cars:        
        car.draw()
    pygame.display.update()
    fps.tick(60)

t = 0
while True:
    update(t)
    render()
    t += float(fps.get_time() / 5000.0)

