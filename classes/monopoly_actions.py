import random
from classes.state import State


class Actions:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def buy_property(self, player, prop, cost=None):
        if prop.is_property and not prop.has_owner() and prop.owner is not player and player.money > prop.cost:
            prop.owner = player
            if cost is None:
                cost = prop.cost
            player.money -= cost
            player.properties.append(prop)
            if self.verbose:
                print("%s buys property %s for $%d" % (player.name, prop.desc(), cost))
                print("%s's new balance: $%d" % (player.name, player.money))
            return True
        return False

    def unmortgage_property(self, player, prop):
        if prop.is_property and prop.owner is player and prop.mortgaged and player.money > prop.mortgage_cost * 1.1:
            prop.mortgaged = False
            player.money -= prop.mortgage_cost * 1.1
            if self.verbose:
                print("%s unmortgages property %s for $%d" % (player.name, prop.desc(), prop.mortgage_cost * 1.1))
                print("%s's new balance: $%d" % (player.name, player.money))
            return True
        return False

    def build_on_area(self, player, group, game):
        if group.is_color and group.owner() is player and player.money > group.building_cost:
            props = sorted(reversed(group.properties), key=lambda x: x.buildings)
            prop_to_build = props[0]
            if prop_to_build.buildings < 4 and game.houses > 0:
                game.houses -= 1
                prop_to_build.buildings += 1
                player.money -= group.building_cost
                if self.verbose:
                    print("%s builds a house on %s for $%d" % (player.name, prop_to_build.desc(), group.building_cost))
                    print("%s's new balance: $%d" % (player.name, player.money))
                return True
            elif prop_to_build.buildings == 4 and game.hotels > 0:
                game.hotels -= 1
                game.houses += 4
                prop_to_build.buildings += 1
                player.money -= group.building_cost
                if self.verbose:
                    print("%s builds a hotel on %s for $%d" % (player.name, prop_to_build.desc(), group.building_cost))
                    print("%s's new balance: $%d" % (player.name, player.money))
                return True
        return False

    def mortgage_property(self, player, prop):
        if prop.is_property and prop.owner is player and not prop.group.has_buildings() and not prop.mortgaged:
            prop.mortgaged = True
            player.money += prop.mortgage_cost
            if self.verbose:
                print("%s mortgages %s for $%d" % (player.name, prop.desc(), prop.mortgage_cost))
                print("%s's new balance: $%d" % (player.name, player.money))
            return True
        return False

    def sell_on_area(self, player, group, game):
        if group.is_color and group.owner() is player:
            props = sorted(reversed(group.properties), key=lambda x: x.buildings, reverse=True)
            prop_to_sell = props[0]
            if 0 < prop_to_sell.buildings < 5:
                game.houses += 1
                prop_to_sell.buildings -= 1
                player.money += 0.5 * group.building_cost
                if self.verbose:
                    print("%s sells house of %s for $%d" % (player.name, prop_to_sell.desc(), group.building_cost * 0.5))
                    print("%s's new balance: $%d" % (player.name, player.money))
                return True
            elif prop_to_sell.buildings == 5 and game.houses >= 4:
                game.hotels += 1
                game.houses -= 4
                prop_to_sell.buildings -= 1
                player.money += 0.5 * group.building_cost
                if self.verbose:
                    print("%s sells hotel of %s for $%d" % (player.name, prop_to_sell.desc(), group.building_cost * 0.5))
                    print("%s's new balance: $%d" % (player.name, player.money))
                return True
        return False

    def pay_money(self, amount, player, target, game):
        if player.money < amount:
            can_sell = True
            while player.money < amount and can_sell:
                can_sell = self.sell_property(player, game)
            if player.money < amount:
                self.bankrupt(player, target, game)
                return False

        player.money -= amount
        if self.verbose:
            target_name = "The Bank" if target is None else target.name
            print("%s pays $%d to %s" % (player.name, amount, target_name))
            print("%s's new balance: $%d" % (player.name, player.money))
        if target is not None:
            target.money += amount
            if self.verbose:
                print("%s's new balance: $%d" % (target.name, target.money))
        return True

    def sell_property(self, player, game):
        done = False
        for group in reversed(game.groups):
            if self.sell_on_area(player, group, game):
                done = True
                break
        if not done:
            for prop in sorted(player.properties, key=lambda x: x.mortgage_cost, reverse=True):
                if self.mortgage_property(player, prop):
                    done = True
                    break
        return done

    def bankrupt(self, player, target, game):
        player.bankrupt = True
        if self.verbose:
            print("%s goes bankrupt" % player.name)
        if target is not None:
            target.properties += player.properties
            target.money += player.money
        else:
            for prop in player.properties:
                self.auction(prop, game)

    def send_to_jail(self, player):
        player.current_pos = 10
        player.in_jail = True
        if self.verbose:
            print("%s was sent to jail" % player.name)

    def roll_dices(self):
        random.seed()
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        if self.verbose:
            print("Dices rolled: %d + %d = %d" % (dice1, dice2, dice1+dice2))
        return dice1, dice2

    def move_player(self, player, dices=None, position=None):
        last_pos = player.current_pos
        if dices is not None:
            player.current_pos += dices
            player.current_pos %= 40
        elif position is not None:
            player.current_pos = position

        if last_pos > player.current_pos:
            player.money += 200
            if self.verbose:
                print("%s collects %d for passing GO" % (player.name, 200))

    def auction(self, prop, game):
        players = game.players_not_in_bankrupt()
        if prop.is_property and not prop.has_owner():
            if self.verbose:
                print("Auction for %s started" % prop.desc())
            bidder = -1
            m = 0.4

            while m >= 0:
                for player in players:
                    bid = prop.cost*m
                    state = State(player, game).get_state_taking_money(bid, prop.group)
                    action = player.policy(state)
                    if action == 1 and player.money >= bid:
                        if self.verbose:
                            print("%s bids %d$ for property %s" % (player.name, bid, prop.desc()))
                        bidder = player
                        break
                if bidder == -1:
                    m -= 0.1
                else:
                    break

            if bidder == -1:
                bidder = random.choice(players)

            i = players.index(bidder)
            bid = -1
            while True:
                i = (i + 1) % len(players)
                player = players[i]
                if player is bidder:
                    break
                bid = prop.cost*m
                state = State(player, game).get_state_taking_money(bid, prop.group)
                action = player.policy(state)
                if action == 1 and player.money >= bid:
                    if self.verbose:
                        print("%s bids %d$ for property %s" % (player.name, bid, prop.desc()))
                    bidder = player
                    m += 0.2

            if self.verbose:
                print("%s won auction for %s" % (player.name, prop.desc()))

            self.buy_property(bidder, prop, bid)

            for player in players:
                reward = game.calc_reward(player)
                new_state = State(player, game).get_state(prop.group)
                player.receive_reward(reward, new_state)

    def draw_from_deck(self, player, deck):
        card = deck.pop(0)
        deck.append(card)
        if self.verbose:
            print("%s draws card: %s" % (player.name, card.name))
        return card

    def check_pos(self, player, game, dices=None):
        card_landed = game.board[player.current_pos]
        if self.verbose:
            print("%s has landed on %s" % (player.name, card_landed.desc()))

        if card_landed.is_property and card_landed.has_owner() and card_landed.owner is not player and not card_landed.mortgaged:
            rent = card_landed.calc_rent(dices)
            game.acts.pay_money(rent, player, card_landed.owner, game)
        elif card_landed.is_tax:
            game.acts.pay_money(card_landed.tax, player, None, game)
        elif card_landed.is_go_jail:
            game.acts.send_to_jail(player)
        elif card_landed.is_community:
            card = self.draw_from_deck(player, game.community_cards)
            card.apply(game)
        elif card_landed.is_chance:
            card = self.draw_from_deck(player, game.chance_cards)
            card.apply(game)
            
    def try_to_escape_jail(self, player, dice1, dice2, game):
        if dice1 == dice2:
            player.in_jail = False
            player.turns_in_jail = 0
            if self.verbose:
                print("%s rolled doubles and has been released from jail" % player.name)
        else:
            player.turns_in_jail += 1
            if player.turns_in_jail == 3:
                if self.verbose:
                    print("%s didn't rolled doubles in three turns and paid 50$ to be released" % player.name)
                player.in_jail = False
                player.turns_in_jail = 0
                self.pay_money(amount=50, player=player, target=None, game=game)
            elif self.verbose:
                print("%s's turns in prison: %d" % (player.name, player.turns_in_jail))






















