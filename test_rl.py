import numpy as np
import torch

from auction.rl import REINFORCEAgent

class MockEnv(object):
    def reset(self):
        pass
    
    def observe(self):
        return np.random.random(7)    

    def try_bid(self, a):
        return 1.0, False

agent = REINFORCEAgent(7, 1)
env = MockEnv()

states = []
actions = []
action_log_probs = []
rewards = []
dones = []

for t in range(10):
    s = env.observe()
    action, action_log_prob = agent.act(s)
    r, d = env.try_bid(action)
    states.append(s)
    actions.append(action)
    action_log_probs.append(action_log_prob)
    rewards.append(r)
    dones.append(d)

agent.train(states=states, actions=actions, log_probs=action_log_probs, rewards=rewards, dones=dones)
    
