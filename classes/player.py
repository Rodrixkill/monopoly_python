import random
import numpy as np
import tensorflow as tf
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
    def __init__(self, name, model, target_model, lr=0.01, gamma=0.9, eps=0.5, eps_decay=0.9999, eps_min=0.1, tau=0.125,
                 batch_size=32, min_experiences=100, max_experiences=1000, num_actions=3):
        Player.__init__(self, name)
        self.eps = eps
        self.model = model
        self.target_model = target_model
        self.optimizer = tf.optimizers.Adam(lr)
        self.gamma = gamma
        self.eps = eps
        self.eps_min = eps_min
        self.eps_decay = eps_decay
        self.tau = tau
        self.batch_size = batch_size
        self.min_experiences = min_experiences
        self.last_action = None
        self.last_state = None
        self.memory = deque(maxlen=max_experiences)
        self.training = False
        self.num_actions = num_actions

    def policy(self, state):
        self.eps *= self.eps_decay
        self.last_state = state
        if self.training and np.random.random() < max(self.eps, self.eps_min):
            self.last_action = np.random.randint(self.num_actions)
        else:
            self.last_action = np.argmax(self.model.predict(self.last_state))
        return self.last_action

    def receive_reward(self, reward, new_state, done=False):
        state = [x for x in self.last_state]
        if new_state is None:
            new_state = [0] * len(state)
        self.memory.append([state, self.last_action, reward, new_state, done])
        self.train()

    def train(self):
        if self.training and len(self.memory) >= self.min_experiences:
            self.model_train()
            self.target_train()

    def model_train(self):
        samples = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = tuple([np.array(x.tolist()) for x in np.array(samples).T])
        # print("States:", states.shape)
        # print("Actions:", actions.shape)
        # print("Rewards:", rewards.shape)
        # print("Next States:", next_states.shape)
        # print(next_states.tolist())
        # print("Dones:", dones.shape)
        value_next = np.max(self.target_model.predict(next_states.reshape(self.batch_size, -1)), axis=1)
        actual_values = np.where(dones, rewards, rewards+self.gamma*value_next)

        with tf.GradientTape() as tape:
            selected_action_values = tf.math.reduce_sum(
                  self.model.predict(states) * tf.one_hot(actions, self.num_actions), axis=1)
            loss = tf.math.reduce_mean(tf.square(actual_values - selected_action_values))
        variables = self.model.trainable_variables
        gradients = tape.gradient(loss, variables)
        self.optimizer.apply_gradients(zip(gradients, variables))
        return loss

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

