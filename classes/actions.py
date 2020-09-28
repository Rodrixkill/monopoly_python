from classes.card_definitions import Card
from classes.player_definitions import Player


class Action:

    def __init__(self, player: Player):
        self.player = player

    def do(self, verbose):
        pass

    def peek_state(self, state):
        pass


class ActionOnProperty(Action):
    def __init__(self, player: Player, prop: Card):
        self.prop = prop
        Action.__init__(self, player)


class BuyProperty(ActionOnProperty):

    def do(self, verbose):
        self.player.buy_property(self.prop)
        if verbose:
            print('%s buys property %s for %d' % (self.player.name, self.prop, self.prop.card_cost))
            print('%s\'s new balance: %d' % (self.player, self.player.balance))

    def peek_state(self, state):
        # return state.add_property(player, prop)
        pass


class MortgageProperty(ActionOnProperty):

    def do(self, verbose):
        self.prop.mortgage(self.player)
        print('%s mortgages property %s for %d' % (self.player.name, self.prop, self.prop.mortgage_amt))
        print('%s\'s new balance: %d' % (self.player, self.player.balance))


class BuyMortgageProperty(ActionOnProperty):

    def do(self, verbose):
        self.prop.buy_mortgage(self.player)
        print('%s pays mortgage of  property %s for %d' % (self.player.name, self.prop, self.prop.mortgage_amt * 1.1))
        print('%s\'s new balance: %d' % (self.player, self.player.balance))


class PayRent(ActionOnProperty):

    def do(self, verbose):
        self.player.charge_rent(self.prop)
        print('%s pays rent of property %s of %d, owned by %s'
              % (self.player.name, self.prop, self.prop.rent_prices[0], self.prop.owner))
        print('%s\'s new balance: %d' % (self.player, self.player.balance))


class LeaveJailPaying(Action):

    def do(self, verbose):
        self.player.release_from_jail_paying()
        print('%s pays 50$ to leave jail' % self.player.name)
        print('%s\'s new balance: %d' % (self.player, self.player.balance))


class LeaveJailRolling(Action):

    def do(self, verbose):
        self.player.release_from_jail_by_rolling()
        print('%s rolls to leave jail' % self.player.name)


class EndTurn(Action):

    def do(self, verbose):
        print('%s ends his turn ' % self.player.name)
