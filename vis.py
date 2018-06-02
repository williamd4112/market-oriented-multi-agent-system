import pygame
import sys
import json
import os

from gen_vis import compute_timings, compute
from simulator.city_graph import CityGraph
from config import Config

SCREEN_SIZE = WIDTH, HEIGHT = (1400, 700)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (0, 0, 255)
CIRCLE_RADIUS = 20
SPEED = 0.5

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
        self.color = GREEN
        self.prev_event = None    
    
    def update(self, t):
        global SPEED 
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
                    self.color = GREEN
                if event_name == 'Call' or event_name == 'Return':                            
                    timings = compute_timings(s['start_time'], s['route'], self.speed)
                    print(timings)
                    self.pos = compute(s['route'], timings, t)
                    self.color = RED
                if event_name == 'Shift': 
                    self.pos = [4, 8]
                    self.color = BLUE
                self.prev_event = s                
                break
    def draw(self):        
        global screen
        pos = [int(self.pos[1] * 100), 700 - int(self.pos[0] * 100)]
        print(pos, self.pos)
        pygame.draw.circle(screen, self.color, pos, CIRCLE_RADIUS, 0)

class Grid(object):
    def __init__(self, edges):
        self.edges = edges
   
    def draw(self):
        global screen
        for e in self.edges:
            u = (int(e[0][1] * 100), 700 - int(e[0][0] * 100))
            v = (int(e[1][1] * 100), 700 - int(e[1][0] * 100))
            pygame.draw.line(screen, WHITE, u, (v))

def load(path):
    with open(path, 'r') as f:
        schedule = json.load(f)
    return Car(schedule, 30)
cars = [load(os.path.join('data', 'driver-relative-0-%03d.json' % i)) for i in range(12)]

edges = CityGraph(Config().intersections).edge_poses
grid = Grid(edges)


def update(t):
    for car in cars:
        car.update(t)    

t = 0
def render():
    global t
    screen.fill(BLACK)
    grid.draw()
    for car in cars:        
        car.draw()
    pygame.display.update()
    fps.tick(60)
    t += 1

while True:
    update(t * (SPEED / 30.0))
    render()
    #t += float(fps.get_time() / 2000.0)

