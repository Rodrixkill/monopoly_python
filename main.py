from classes.player_definitions import Player
from classes.game import Game

player1 = Player('Player 1', True)
player2 = Player('Player 2', True)
player3 = Player('Player 3', True)
player4 = Player('Player 4', True)

players = [player1, player2, player3, player4]

game = Game(players, verbose=True)

game.play()