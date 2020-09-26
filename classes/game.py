from typing import List

from classes.player_definitions import Player

NUM_PLAYERS = 4
TURN_LIMIT = 100


class Game:
    def __init__(self, players: List[Player]):
        self.players: List[Player] = players
        self.board = [] #TODO implement
        self.turns = 0
        self.current_player = 0
        self.doubles_counter = 0

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

    def end_turn(self):
        self.current_player += 1
        self.current_player %= NUM_PLAYERS

    def play(self, verbose=False):
        while not self.game_over():
            self.players[self.current_player].take_action(self)

        if verbose:
            print("%s wins!" % self.winner().name)

    def actions(self):
        pass