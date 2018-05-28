import json
import os

if __name__ == '__main__':
    path = os.path.join('data', 'driver_0.json')
    with open(path, 'r') as f:
        obj = json.load(f)
    for o in obj:
        print(o)
