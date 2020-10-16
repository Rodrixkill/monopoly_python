from typing import List, Any, Union

from classes.state import State
from classes.rl_actions import SPEND, GET_MONEY, DO_NOTHING
from game.board_init import initialize_board
from game.fortune_init import initialize_chance_cards, initialize_community_cards
from classes.monopoly_actions import Actions
from classes.rl_actions import RLActions

MAX_ACTIONS_PER_GROUP = 3
TURN_LIMIT = 100
MAX_HOUSES = 25
MAX_HOTELS = 10
WIN_REWARD = 10
DEFEAT_REWARD = -10


class Game:
    def __init__(self, players, verbose=False):
        self.players = players
        self.bankrupt_players = []
        self.board, self.groups = initialize_board()
        self.chance_cards = initialize_chance_cards()
        self.community_cards = initialize_community_cards()
        self.turns = 0
        self.player_index = 0
        self.doubles_counter = 0
        self.verbose = verbose
        self.houses = MAX_HOUSES
        self.hotels = MAX_HOTELS
        self.acts: Actions = Actions(verbose)
        self.rl_acts: RLActions = RLActions(game=self)

    def smooth_function(self, x):
        return x / (1 + abs(x))

    def players_not_in_bankrupt(self):
        return [player for player in self.players if not player.bankrupt]

    def game_over(self):
        return self.turns >= TURN_LIMIT or len(self.players_not_in_bankrupt()) == 1

    def winner(self):
        assert (self.game_over())
        players = self.players_not_in_bankrupt()
        if len(players) == 1:
            return players[0]
        else:
            richest_players = sorted(self.players, key=lambda x: x.total_net_worth(), reverse=True)
            return richest_players[0]

    def calc_reward(self, player):
        p = len(self.players_not_in_bankrupt())
        c = 1 / len(self.players_not_in_bankrupt())
        m = player.money / sum([p.money for p in self.players])

        props = [card for card in self.board if card.is_property and card.has_owner()]
        v = sum([(prop.buildings+1) * (1 if prop.owner is player else -1) for prop in props])
        return self.smooth_function((v*c)/p) + (1/p)*m

    def play(self):
        for player in self.players:
            player.reset()

        while not self.game_over():
            player = self.players[self.player_index]
            self.play_turn(player)
            self.turns += 1
            if self.doubles_counter == 0:
                self.player_index = (self.player_index + 1) % len(self.players)
            if self.verbose:
                input()

        winner = self.winner()
        winner.receive_reward(WIN_REWARD, None, done=True)
        for player in self.players:
            if player is not winner:
                player.receive_reward(DEFEAT_REWARD, None, done=True)

        if self.verbose:
            print("%s wins!" % winner.name)
        return winner

    def make_actions(self, player):
        temp_pos = player.current_pos
        while not self.board[temp_pos].is_property:
            temp_pos += 1
        card = self.board[temp_pos]
        index_group = self.groups.index(card.group)
        groups = self.groups[index_group:] + self.groups[:index_group]
        place = self.board[player.current_pos]
        for i in range(MAX_ACTIONS_PER_GROUP):
            for group in groups:
                if group.num_owned(player) == 0 and not (place.is_property and place.group is group):
                    continue
                state = State(player, self).get_state(group)
                action = player.policy(state)
                self.rl_acts.do_action(player, action, group)
                new_state = State(player, self).get_state(group)
                reward = self.calc_reward(player)
                player.receive_reward(reward, new_state)

        player.train()

    def play_turn(self, player):
        if player.bankrupt:
            return
        if self.verbose:
            print("%s's turn" % player.name)
            print("%s's balance: %d" % (player.name, player.money))

        dice1, dice2 = self.acts.roll_dices()
        if player.in_jail:
            self.acts.try_to_escape_jail(player, dice1, dice2, self)

        if player.in_jail or player.bankrupt:
            return

        if dice1 == dice2:
            self.doubles_counter += 1
            if self.doubles_counter == 3:
                self.doubles_counter = 0
                self.acts.send_to_jail(player)
                return
        else:
            self.doubles_counter = 0

        self.acts.move_player(player, dices=dice1+dice2)
        self.acts.check_pos(player, self, dices=dice1+dice2)

        if not player.bankrupt and not player.in_jail:
            self.make_actions(player)

        place_landed = self.board[player.current_pos]
        if place_landed.is_property and not place_landed.has_owner():
            self.acts.auction(place_landed, self)





