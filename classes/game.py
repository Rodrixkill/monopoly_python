from typing import List

from classes.player_definitions import Player
from classes.card_definitions import Card
from classes.fortune_definitions import Fortune
from game.information import initialize_cards_and_board
from game.community_cards import initialize_community_cards
from game.fortune_cards import initialize_fortune_cards
import classes.actions as acts

NUM_PLAYERS = 4
TURN_LIMIT = 10000


class Game:
    def __init__(self, players: List[Player], verbose=False):
        self.players: List[Player] = players
        self.board: List[Card] = initialize_cards_and_board()
        self.turns = 0
        self.player_index = -1
        self.doubles_counter = 0
        self.amount_to_pay = 0
        self.actual_bid = 0
        self.verbose = verbose

    def players_not_in_bankruptcy(self):
        return [player for player in self.players if not player.bankruptcy]

    def game_over(self):
        return self.turns >= TURN_LIMIT or len(self.players_not_in_bankruptcy()) == 1

    def winner(self) -> Player:
        assert (self.game_over())
        players_not_in_bankruptcy = self.players_not_in_bankruptcy()
        if len(players_not_in_bankruptcy) == 1:
            return players_not_in_bankruptcy[0]
        else:
            richest_players = sorted(self.players, key=lambda x: x.total_net_worth(), reverse=True)
            return richest_players[0]

    def play(self):
        for player in self.players:
            player.reset()

        while not self.game_over():
            player = self.players[self.player_index]

            self.play_turn(player)

        if self.verbose:
            print("%s wins!" % self.winner().name)

    def play_turn(self, player):
        if player.in_jail:
            actions = [acts.LeaveJailPaying(player), acts.LeaveJailRolling(player)]
            action = player.take_action(actions)
            action.do()
            if self.verbose:
                action.describe()
            return

        dice1, dice2 = player.roll_dice()
        if self.verbose:
            print('%d rolls %d and %d. Total: %d' % (player.name, dice1, dice2, dice1 + dice2))
        if dice1 == dice2:
            self.doubles_counter += 1
        else:
            self.doubles_counter = 0

        if self.doubles_counter == 3:
            self.doubles_counter = 0
            self.player_index = (self.player_index + 1) % 4
            player.send_to_jail()
            if self.verbose:
                print('%s was sent to jail for rolling doubles three times in a row' % player.name)
            return

        last_pos = player.current_pos
        player.move_player(dice1 + dice2)

        if player.current_pos < last_pos:
            player.add_balance(200)
            if self.verbose:
                print('%s receives 200$ for passing GO' % player.name)

        prop_landed = self.board[player.current_pos]
        if self.verbose:
            print('%s landed on %s' % (player.name, prop_landed))

        actions: List[acts.Action] = [acts.BuyMortgageProperty(player, prop)
                                      if prop.mortgaged else acts.MortgageProperty(player, prop)
                                      for prop in player.cards_owned]

        tax = 0
        if prop_landed.card_name == 'Luxury Tax':
            tax = 100
        elif prop_landed.card_name == 'Income Tax':
            tax = 200

        while player.balance < tax:
            action = player.take_action(actions)
            actions.remove(action)
            action.do(self.verbose)

        #community


        player.reduce_balance(tax)
        if self.verbose:
            print('%s pays tax of %s$' % (player.name, tax))

        if not prop_landed.has_owner():
            actions.append(acts.BuyProperty(player, prop_landed))
        else:
            actions.append(acts.PayRent(player, prop_landed))

            # while player.balance <= debe:



    def start_auction(self, prop: Card):
        m = 0
        player_index = self.player_index
        winner_index = self.player_index

        if self.verbose:
            print('Auction for %s started at 0, actual winner: %s' % (prop, self.players[winner_index].name))

        while True:
            player_index = (player_index + 1) % 4
            if player_index == winner_index:
                break

            player = self.players[player_index]
            if player.want_to_bid(prop, int(prop.card_cost * (m + 0.2))):
                winner_index = player_index
                m += 0.2
                if self.verbose:
                    print('%s bids for %s with %d' % (player.name, prop, int(prop.card_cost * m)))

        winner = self.players[winner_index]
        if self.verbose:
            print('%s wins auction for %s with %d' % (winner.name, prop, int(prop.card_cost * m)))
        winner.buy_property_to_price(prop, int(prop.card_cost * m))
