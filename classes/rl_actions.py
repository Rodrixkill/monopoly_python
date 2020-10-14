from classes.monopoly_actions import Actions

DO_NOTHING = 0
SPEND = 1
GET_MONEY = 2


class RLActions:

    def __init__(self, game):
        self.acts = Actions(game.verbose)
        self.game = game
        self.verbose = game.verbose

    def do_action(self, player, action, group):
        assert (action in [SPEND, GET_MONEY, DO_NOTHING])
        if action == SPEND:
            if self.verbose:
                print("%s will try to spend on group %s" % (player.name, group.color))
            self.spend(player, group)
        elif action == GET_MONEY:
            if self.verbose:
                print("%s will try to gain money from group %s" % (player.name, group.color))
            self.get_money(player, group)
        else:
            if self.verbose:
                print("%s will not do any action on group %s" % (player.name, group.color))

    def spend(self, player, group):
        prop = self.game.board[player.current_pos]
        if prop in group.properties:
            property_bought = self.acts.buy_property(player, prop)
            if property_bought:
                return

        for prop in reversed(group.properties):
            property_unmortgaged = self.acts.unmortgage_property(player, prop)
            if property_unmortgaged:
                return

        building_built = self.acts.build_on_area(player, group, self.game)
        if not building_built and self.verbose:
            print("%s couldn't spend on group %s" % (player.name, group.color))

    def get_money(self, player, group):
        building_sold = self.acts.sell_on_area(player, group, self.game)
        if building_sold:
            return
        for prop in reversed(group.properties):
            property_mortgaged = self.acts.mortgage_property(player, prop)
            if property_mortgaged:
                return
        if self.verbose:
            print("%s couldn't get money from group %s" % (player.name, group.color))









