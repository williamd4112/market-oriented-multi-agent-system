import pygame
import sys
import json
import os

from gen_vis import compute_timings, compute
from simulator.city_graph import CityGraph
from config import Config

SCALE = 100
SCREEN_SIZE = WIDTH, HEIGHT = (14 * SCALE, 7 * SCALE)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (0, 0, 255)

CIRCLE_RADIUS = 20
SPEED = 0.6

# Initialization
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Visualization')
fps = pygame.time.Clock()
paused = False

def convert_pos(pos):
    global SCALE, HEIGHT
    return [int(pos[1] * SCALE), HEIGHT - int(pos[0] * SCALE)]

class Car(object):
    def __init__(self, schedule, speed):
        self.schedule = schedule
        self.speed = speed
        self.pos = [4, 8]
        self.color = GREEN
        self.prev_event = None    
    
    def update(self, t):
        global SPEED 
        for s in self.schedule:   
            if t >= s['start_time'] and t < s['end_time']:
                event_name = s['event_name']
                if event_name == 'Free':
                    if self.prev_event is None:
                        self.pos = [4, 8]
                    elif self.prev_event['event_name'] == 'Call' or self.prev_event['event_name'] == 'Return':
                        self.pos = self.prev_event['route'][-1]
                    self.color = GREEN
                if event_name == 'Call' or event_name == 'Return':                            
                    timings = compute_timings(s['start_time'], s['route'], self.speed)
                    self.pos = compute(s['route'], timings, t)
                    self.color = RED
                if event_name == 'Shift': 
                    self.pos = [4, 8]
                    self.color = BLUE
                self.prev_event = s                
                break
    def draw(self):        
        pos = convert_pos(self.pos)
        pygame.draw.circle(screen, self.color, pos, CIRCLE_RADIUS, 0)

class Grid(object):
    def __init__(self, edges):
        self.edges = edges
   
    def draw(self):
        global screen
        for e in self.edges:
            u = convert_pos(e[0])
            v = convert_pos(e[1])
            pygame.draw.line(screen, WHITE, u, (v))

def draw_calls(t, calls):
    eps = (SPEED / 30.0)
    for call in calls:
        if abs(call['time'] - t) < eps:
            color = (255, 255, 0) if call['accept'] else (255, 0, 255)            
            pygame.draw.circle(screen, color, convert_pos(call['start_pos']), 10, 0)
        if call['time'] > t + eps:
            break

def load(path):
    with open(path, 'r') as f:
        schedule = json.load(f)
    return Car(schedule, 30)

def load_call(path):
    with open(path, 'r') as f:
        calls = json.load(f)
    return calls

cars = [load(os.path.join('data', 'driver-relative-0-%03d.json' % i)) for i in range(12)]
calls = load_call(os.path.join('data', 'history-calls.json'))
edges = CityGraph(Config().intersections).edge_poses
grid = Grid(edges)


def update(t):
    print(t)
    for car in cars:
        car.update(t)    
t = 0
def render():
    global t
    screen.fill(BLACK)
    grid.draw()
    draw_calls(t * (SPEED / 30.0), calls)
    for car in cars:        
        car.draw()
    pygame.display.update()
    fps.tick(60)
    t += 1

while True:
    update(t * (SPEED / 30.0))
    render()

