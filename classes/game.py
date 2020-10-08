from typing import List, Any, Union

from classes.player import Player
from classes.card import Card
from classes.fortune_definitions import Fortune
from game.board_init import initialize_board
from game.community_cards import initialize_community_cards
from game.fortune_cards import initialize_fortune_cards
import classes.monopoly_actions as acts
import random

NUM_PLAYERS = 4
TURN_LIMIT = 10000
MAX_HOUSES = 25
MAX_HOTELS = 10


def smooth_function(x: float):
    return x / (1 + abs(x))


class Game:
    def __init__(self, players: List[Player], verbose=False):
        self.players: List[Player] = players
        self.board: List[Card] = initialize_board()
        self.fortune_cards: List[Fortune] = initialize_fortune_cards()
        self.community_cards: List[Fortune] = initialize_community_cards()
        self.turns = 0
        self.player_index = 0
        self.doubles_counter = 0
        self.verbose = verbose
        self.houses = MAX_HOUSES
        self.hotels = MAX_HOTELS

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
                    print('%s\'s balance: %d' % (player.name, player.balance))
            # if self.verbose:
            #     input()

        if self.verbose:
            print("%s wins!" % self.winner().name)

    def play_turn_in_jail(self, player):
        pass

    def play_turn(self, player):
        if player.bankruptcy:
            return

        dice1, dice2 = player.roll_dice()
        if self.verbose:
            print('%s rolls %d and %d. Total: %d' % (player.name, dice1, dice2, dice1 + dice2))
        if dice1 == dice2:
            self.doubles_counter += 1
        else:
            self.doubles_counter = 0

        if self.doubles_counter == 3:
            player.send_to_jail()
            if self.verbose:
                print('%s was sent to jail for rolling doubles three times in a row' % player.name)
            return

        player.move_player(dice1 + dice2)
        prop_landed = self.board[player.current_pos]
        if self.verbose:
            print('%s landed on %s' % (player.name, prop_landed))





        turn_ended = False
        self.doubles_counter = 0
        while not turn_ended:

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

            if prop_landed.owner_is_bank():
                card_name = prop_landed.card_name
                if card_name == 'Luxury Tax' or card_name == 'Income Tax':
                    tax = 100 if card_name == 'Luxury Tax' else 200
                    player.reduce_balance(tax)
                    print('%s pays tax of %s$' % (player.name, tax))
                elif card_name == 'Community Chest' or card_name == 'Chance':
                    cards = self.fortune_cards if card_name == 'Chance' else self.community_cards
                    card: Fortune = random.choice(cards)
                    if self.verbose:
                        print('%s draws card: %s' % (player.name, card.description))
                    card.play(player, [p for p in self.players if p is not player])
                elif card_name == 'Go to Jail':
                    print('%s goes to jail' % player.name)
                elif card_name != 'Go' and card_name != 'Jail/Visiting Jail' and card_name != 'Free Parking':
                    actions.append(acts.BuyProperty(player, prop_landed))
            elif prop_landed.owner is not player:
                actions.append(acts.PayRent(player, prop_landed))

            end_turn_action = acts.EndTurn(player)
            action = None
            actions.append(end_turn_action)
            while action is not end_turn_action:
                action = player.take_action(actions)
                actions.remove(action)
                action.do(self.verbose)

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
