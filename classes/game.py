from typing import List

from classes.player_definitions import Player
from game.information import initialize_cards_and_board

NUM_PLAYERS = 4
TURN_LIMIT = 100
BIDDING, PAYING, NEXT_TURN = 10, 20, 30


class Game:
    def __init__(self, players: List[Player]):
        self.players: List[Player] = players
        self.board = initialize_cards_and_board()
        self.turns = 0
        self.player_index = -1
        self.doubles_counter = 0
        self.state = NEXT_TURN
        self.amount_to_pay = 0

    def players_not_in_bankruptcy(self):
        return [player for player in self.players if not player.bankruptcy]

    def game_over(self):
        return self.turns >= TURN_LIMIT or len(self.players_not_in_bankruptcy()) == 1

    def winner(self) -> Player:
        assert(self.game_over())
        players_not_in_bankruptcy = self.players_not_in_bankruptcy()
        if len(players_not_in_bankruptcy) == 1:
            return players_not_in_bankruptcy[0]
        else:
            max_money = float('-inf')
            richest_player = None
            for player in self.players:
                if player.balance > max_money:
                    max_money = player.balance
                    richest_player = player
            return richest_player

    def play(self, verbose=False):
        while not self.game_over():
            if self.state is NEXT_TURN:
                self.player_index = (self.player_index + 1) % NUM_PLAYERS
            player = self.players[self.player_index]
            dice1, dice2 = player.roll_dice()
            if dice1 == dice2:
                self.doubles_counter += 1

            if self.doubles_counter == 3:
                self.doubles_counter = 0
                player.send_to_jail()
                continue

            player.move_player(dice1 + dice2)
            action = player.take_action(self)


        if verbose:
            print("%s wins!" % self.winner().name)

    def actions(self):
        pass