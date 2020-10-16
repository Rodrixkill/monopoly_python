from classes.player import RandomAgent, FixedPolicyAgent, RLAgent
from classes.game import Game
import random
import tensorflow as tf
import numpy as np
from time import time


class MyModel(tf.keras.Model):
    def __init__(self, input_size, hidden_units, num_actions):
        super(MyModel, self).__init__()
        self.input_size = input_size
        self.input_layer = tf.keras.layers.InputLayer(input_shape=(input_size,))
        self.hidden_layers = []
        for i in hidden_units:
            self.hidden_layers.append(tf.keras.layers.Dense(
                i, activation='relu', kernel_initializer='RandomNormal'))
        self.output_layer = tf.keras.layers.Dense(
            num_actions, activation='linear', kernel_initializer='RandomNormal')

    def predict(self, inputs):
        if type(inputs) != np.array:
            inputs = np.array(inputs)
        inputs = inputs.reshape(-1, self.input_size)
        z = self.input_layer(inputs)
        for layer in self.hidden_layers:
            z = layer(z)
        output = self.output_layer(z)
        return output


def test_players(players, total_games, verbose=False):
    num_wins = [0] * len(players)
    for i in range(total_games):
        if i % 10 == 0:
            print("Episodes:", i)
        game = Game(random.sample(players, len(players)), verbose=verbose)
        winner = game.play()
        num_wins[players.index(winner)] += 1

    for i in range(len(players)):
        print(players[i].name, ": ", num_wins[i] / total_games)


random_agent = RandomAgent("RandomAgent")
fixed_agent = FixedPolicyAgent("FixedPolicyAgent", max_get_money=150, min_spend=350)
rlagent = RLAgent("RLAgent", model=MyModel(23, [20, 20], 3), target_model=MyModel(23, [20, 20], 3))
start_time = time()
# #
# test_players([random_agent, fixed_agent], 100, False)
# rlagent.training = False
# # test_players([fixed_agent, random_agent], 10)
rlagent.training = False
test_players([rlagent, fixed_agent, random_agent], 100)
rlagent.training = True
test_players([rlagent, fixed_agent], 100)
rlagent.training = False
test_players([rlagent, fixed_agent, random_agent], 100)
elapsed_time = time() - start_time
print("Elapsed time: %0.10f seconds." % elapsed_time)
