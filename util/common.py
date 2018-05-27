import numpy as np

def check_duplicated_element(l):
    return len(l) != len(set(l))

def movement_to_dir(mov):
    direction = (np.sign(mov[0]), np.sign(mov[1]))
    return direction
 
