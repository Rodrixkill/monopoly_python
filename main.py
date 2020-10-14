from classes.player import RandomAgent, FixedPolicyAgent, RLAgent
from classes.game import Game
import random
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam


def test_players(players, total_games, verbose=False):
    num_wins = [0] * len(players)
    for i in range(total_games):
        if i % 1 == 0:
            print(i)
        game = Game(random.sample(players, len(players)), verbose=verbose)
        winner = game.play()
        num_wins[players.index(winner)] += 1

    for i in range(len(players)):
        print(players[i].name, ": ", num_wins[i] / total_games)


def create_model(input_size=23, num_actions=3, learning_rate=0.05):
    model = Sequential()
    model.add(Dense(24, input_dim=input_size, activation="relu"))
    model.add(Dense(48, activation="relu"))
    model.add(Dense(24, activation="relu"))
    model.add(Dense(num_actions))
    model.compile(loss="mean_squared_error",
                  optimizer=Adam(lr=learning_rate))
    return model


random_agent = RandomAgent("RandomAgent")
fixed_agent = FixedPolicyAgent("FixedPolicyAgent", max_get_money=150, min_spend=350)
rlagent = RLAgent("RLAgent", model=create_model(), target_model=create_model())

# test_players([random_agent, fixed_agent], 100)
rlagent.training = True
test_players([fixed_agent, rlagent], 1000)
# rlagent.training = False
# test_players([random_agent, fixed_agent, rlagent], 100)
