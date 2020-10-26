from classes.player import RandomAgent, FixedPolicyAgent, RLAgent
from classes.game import Game
import random
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from time import time

class MyModel(tf.keras.Model):
    def __init__(self, input_size, hidden_units, num_actions):
        super(MyModel, self).__init__()
        self.input_size = input_size
        self.input_layer = tf.keras.layers.InputLayer(input_shape=(input_size,))
        self.hidden_layers = []
        for i in hidden_units:
            self.hidden_layers.append(tf.keras.layers.Dense(
                i, activation='relu', kernel_initializer='Zeros'))
        self.output_layer = tf.keras.layers.Dense(
            num_actions, activation='linear', kernel_initializer='Zeros')

    def predict(self, inputs):
        if type(inputs) != np.array:
            inputs = np.array(inputs)
        inputs = inputs.reshape(-1, self.input_size)
        z = self.input_layer(inputs)
        for layer in self.hidden_layers:
            z = layer(z)
        output = self.output_layer(z)
        return output


def test_players(players, total_games, verbose=False, turn_limit=100):
    num_wins = [0] * len(players)
    for i in range(total_games):
        if i % 10 == 0:
            print("Episodes:", i)
        game = Game(random.sample(players, len(players)), verbose=verbose)
        game.turn_limit = turn_limit
        winner = game.play()
        num_wins[players.index(winner)] += 1

    for i in range(len(players)):
        wins_array[i] = num_wins[i] / total_games
        print(players[i].name, ": ", num_wins[i] / total_games)

def smooth_function(x):
        return x / (1 + abs(x))
wins_array= [0] * 2
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
random_agent = RandomAgent("RandomAgent")
agents = ['Fixed Agent', 'RL Agent']
fixed_agent = FixedPolicyAgent("FixedPolicyAgent", max_get_money=150, min_spend=350)
rlagent = RLAgent("RLAgent", model=MyModel(1, [20], 3), target_model=MyModel(1, [20], 3), lr=0.01)
start_time = time()


#Testing
print("Testing")
rlagent.training = False
rlagent.cum_rewards = []
rlagent.sum_rewards = 0
test_players([fixed_agent, rlagent], 100, turn_limit=100)
print("avg reward", sum(rlagent.cum_rewards)/len(rlagent.cum_rewards))

for j in range(0, 2000, 50):
    print(j, ':', rlagent.model.predict([j]).numpy())

for i in range(10):
    # Training
    print("Training")
    rlagent.training = True
    rlagent.eps = 0.3
    test_players([fixed_agent, rlagent], 200, turn_limit=100)


    print("Testing")
    rlagent.training = False
    rlagent.cum_rewards = []
    rlagent.sum_rewards = 0
    test_players([fixed_agent, rlagent], 100, turn_limit=100)
    print("avg reward", sum(rlagent.cum_rewards)/len(rlagent.cum_rewards))

    for j in range(0, 2000, 50):
        print(j, ':', rlagent.model.predict([j]).numpy())


elapsed_time = time() - start_time
print("Elapsed time: %0.10f seconds." % elapsed_time)
ax.bar(agents, wins_array)
plt.show()
