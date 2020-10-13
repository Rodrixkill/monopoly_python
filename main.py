from classes.player import RandomAgent, FixedPolicyAgent
from classes.game import Game
import random


def test_players(players, total_games, verbose=False):
    num_wins = [0] * len(players)
    for i in range(total_games):
        if i % 10 == 0:
            print(i)
        game = Game(random.sample(players, len(players)), verbose=verbose)
        winner = game.play()
        num_wins[players.index(winner)] += 1

    for i in range(len(players)):
        print(players[i].name, ": ", num_wins[i] / total_games)


random_agent = RandomAgent("RandomAgent")
fixed_agent = FixedPolicyAgent("FixedPolicyAgent", min_spend=350, max_get_money=150)
fixed_agent2 = FixedPolicyAgent("FixedPolicyAgent2", min_spend=500, max_get_money=300)
test_players([random_agent, fixed_agent, fixed_agent2], 1, True)
