import numpy as np

import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.nn.utils as utils

from torch.autograd import Variable
from torch.distributions.normal import Normal

'''
Bidding problem can be modeled as a sequential decision problem.
The state is (start_pos_driver, start_pos_call, dest_pos_call, time (24hrs))
The action is [0, 1]
'''

eps = np.finfo(np.float32).eps.item()

class Policy(nn.Module):
    def __init__(self, x_dim, a_dim):
        super(Policy, self).__init__()
        self.phi = nn.Linear(x_dim, 128)
        self.mu = nn.Linear(128, a_dim)
        self.sigma = nn.Linear(128, a_dim)
        self.tanh = nn.Tanh()
        self.softplus = nn.Softplus()

    def forward(self, x):
        out = self.phi(x)
        mu = self.tanh(self.mu(out))
        sigma = self.softplus(self.sigma(out))
        return mu, sigma

class REINFORCEAgent(object):
    def __init__(self, x_dim, a_dim, lr=1e-3, gamma=0.99):
        self.x_dim = x_dim
        self.a_dim = a_dim
        self.lr = lr
        self.gamma = gamma
        self.policy = Policy(self.x_dim, self.a_dim)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=self.lr)

    def act(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0)
        mu, sigma = self.policy(state)
        dist = Normal(mu, sigma)
        action = dist.sample()
        action_log_prob = dist.log_prob(action)
        return action, action_log_prob
                
    def train(self, states, actions, log_probs, rewards, dones):
        R = 0
        policy_loss = []
        discounted_rewards = []
        for r in rewards[::-1]:
            R = r + self.gamma * R
            discounted_rewards.insert(0, R)
            rewards = torch.tensor(rewards)
        discounted_rewards = torch.tensor(discounted_rewards)
        discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + eps)
        for log_prob, discounted_reward in zip(log_probs, discounted_rewards):
            policy_loss.append(-log_prob * discounted_reward)

        self.optimizer.zero_grad()
        policy_loss = torch.cat(policy_loss).sum()
        policy_loss.backward()
        self.optimizer.step()
