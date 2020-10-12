from typing import List, Any, Union

from classes.player import Player
from classes.card import Card
from game.board_init import initialize_board
from game.fortune_init import initialize_chance_cards, initialize_community_cards
from classes.monopoly_actions import Actions

NUM_PLAYERS = 4
TURN_LIMIT = 10000
MAX_HOUSES = 25
MAX_HOTELS = 10


def smooth_function(x: float):
    return x / (1 + abs(x))


class Game:
    def __init__(self, players: List[Player], verbose=False):
        self.players = players
        self.board = initialize_board()
        self.chance_cards = initialize_chance_cards()
        self.community_cards = initialize_community_cards()
        self.turns = 0
        self.player_index = 0
        self.doubles_counter = 0
        self.verbose = verbose
        self.houses = MAX_HOUSES
        self.hotels = MAX_HOTELS
        self.acts: Actions = Actions(verbose)

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
        c = 0.2
        m = player.money / sum([p.money for p in self.players])

        props = [card for card in self.board if card.is_property and card.has_owner()]
        v = [(prop.houses+1) * (1 if prop.owner is player else -1) for prop in props]

        return smooth_function((v*c)/p) + (1/p)*m

    def play(self):
        for player in self.players:
            player.reset()

        while not self.game_over():
            player = self.players[self.player_index]
            self.play_turn(player)
            self.turns += 1
            self.player_index = (self.player_index + 1) % NUM_PLAYERS
            if self.player_index == 0:
                for player in self.players:
                    print('%s\'s balance: %d' % (player.name, player.money))
            # if self.verbose:
            #     input()

        if self.verbose:
            print("%s wins!" % self.winner().name)

    def play_turn(self, player):
        if player.bankruptcy:
            return
        if self.verbose:
            print("%s's turn" % player.name)
            print("%s's balance: %d" % (player.name, player.money))

        dice1, dice2 = self.acts.roll_dices()
        if player.in_jail:
            self.acts.try_to_escape_jail(player, dice1, dice2)

        if player.in_jail or player.bankrupt:
            return

        if dice1 == dice2:
            self.doubles_counter += 1
        else:
            self.doubles_counter = 0

        if self.doubles_counter == 3:
            self.acts.send_to_jail(player)
            return

        self.acts.move_player(player, dices=dice1+dice2)
        self.acts.check_pos(player, self)

        if not player.bankrupt and not player.in_jail:
            pass
            #TODO TAKE ACTION



