import json
import os, sys

if __name__ == '__main__':
    path = os.path.join(sys.argv[1])
    with open(path, 'r') as f:
        obj = json.load(f)
    for o in obj:
        print(o)
