from classes.player import RandomAgent, FixedPolicyAgent
from classes.game import Game

random_agent = RandomAgent("RandomAgent")
fixed_agent = FixedPolicyAgent("FixedPolicyAgent", min_spend=350, max_get_money=150)

random_agent_wins = 0
fixed_policy_agent_wins = 0

# game = Game([random_agent, fixed_agent], verbose=True)
# game.play()

total_games = 1000

for i in range(total_games):
    if i % 100 == 0:
        print(i)
    game = Game([random_agent, fixed_agent], verbose=False)
    winner = game.play()
    if winner is random_agent:
        random_agent_wins += 1
    elif winner is fixed_agent:
        fixed_policy_agent_wins += 1

print("Sum: ", random_agent_wins + fixed_policy_agent_wins)
print("Random wins: ", random_agent_wins/total_games)
print("Fixed wins: ", fixed_policy_agent_wins/total_games)