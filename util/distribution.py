import numpy as np
import random

class NormalDistribution(object):
    def __init__(self, mu=0.0, sigma=1.0):
        self.set(mu, sigma)

    def set(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def __call__(self):
        # TODO: Change to Box-Muller in final version
        # TODO: Handle negative distance
        return np.clip(np.random.normal(self.mu, self.sigma), 0.5, 3.5)

class PoissonProcess(object):
    def __init__(self, lambd=1.0/40.0):
        self.set(lambd)

    def set(self, lambd):        
        self.lambd = lambd
    
    def __call__(self):
        return random.expovariate(self.lambd)

