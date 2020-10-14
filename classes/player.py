import random
import numpy as np
from classes.rl_actions import SPEND, GET_MONEY, DO_NOTHING
from collections import deque

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.properties = []
        self.current_pos = 0
        self.in_jail = False
        self.turns_in_jail = 0
        self.bankrupt = False

    def reset(self):
        self.properties = []
        self.money = 1500
        self.current_pos = 0
        self.in_jail = False
        self.turns_in_jail = 0
        self.bankrupt = False

    def total_net_worth(self):
        net_worth = self.money
        for prop in self.properties:
            if prop.mortgaged:
                continue
            net_worth += prop.mortgage_cost
            net_worth += prop.buildings*prop.group.building_cost*0.5
        return net_worth

    def policy(self, state):
        pass

    def receive_reward(self, reward, new_state, done=False):
        pass

    def train(self):
        pass


class RandomAgent(Player):
    def policy(self, state):
        return random.choice([DO_NOTHING, SPEND, GET_MONEY])


class FixedPolicyAgent(Player):
    def __init__(self, name, min_spend, max_get_money):
        Player.__init__(self, name)
        self.min_spend = min_spend
        self.max_get_money = max_get_money

    def policy(self, state):
        if self.money <= self.max_get_money:
            return GET_MONEY
        elif self.money >= self.min_spend:
            return SPEND
        else:
            return DO_NOTHING


class RLAgent(Player):
    def __init__(self, name, model, target_model, gamma=0.9, eps=0.5, eps_decay=0.99, tau=0.125):
        Player.__init__(self, name)
        self.eps = eps
        self.model = model
        self.target_model = target_model
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay
        self.tau = tau
        self.last_action = None
        self.last_state = None
        self.memory = deque(maxlen=2000)
        self.training = False

    def policy(self, state):
        self.eps *= self.eps_decay
        self.last_state = np.array(state).reshape(1, -1)
        if self.training and np.random.random() < self.eps:
            self.last_action = np.random.randint(3)
        else:
            self.last_action = np.argmax(self.model.predict(self.last_state)[0])
        return self.last_action

    def receive_reward(self, reward, new_state, done=False):
        state = np.copy(self.last_state)
        new_state = np.array(new_state).reshape(1, -1)
        self.memory.append((state, self.last_action, reward, new_state, done))

    def train(self):
        if self.training:
            self.model_train()
            self.target_train()

    def model_train(self):
        batch_size = 1
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

