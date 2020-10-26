MAX_MONEY = 1500
MAX_POSITION = 40

class State:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.money = player.money

    def calc_money_to_spend(self, group):
        prop = self.game.board[self.player.current_pos]
        if prop.is_property and not prop.has_owner() and self.money >= prop.cost:
            return prop.cost
        for prop in group.properties:
            if prop.owner is self.player and prop.mortgaged and self.money >= prop.mortgage_cost * 1.1:
                return prop.mortgage_cost * 1.1
        if group.is_color and group.owner() is self.player and self.money >= group.building_cost:
            return group.building_cost
        return 0

    def calc_money_to_get(self, group):
        for prop in group.properties:
            if prop.owner is self.player and not prop.mortgaged:
                return prop.mortgage_cost
        if group.is_color and group.owner() is self.player:
            return 0.5 * group.building_cost
        return 0

    def norm_money(self, money):
        return self.game.smooth_function((money / MAX_MONEY))

    def get_state(self, group, money_to_spend=None, money_to_get=None):
        return [self.money/1500]
        # player_info = 0
        # others_info = 0
        # if group.owner() is None:
        #     group_props = [prop for prop in group.properties if prop.has_owner() and not prop.mortgaged]
        #     player_props = len([prop for prop in group_props if prop.owner is self.player])
        #     others_props = len(group_props) - player_props
        #     x = 12 / group.num_props()
        #     player_info = x * player_props / 17
        #     others_info = x * others_props / 17
        # else:
        #     max_buildings = max([prop.buildings for prop in group.properties])
        #     if group.owner() is self.player:
        #         player_info = (12 + max_buildings) / 17
        #     else:
        #         others_info = (12 + max_buildings) / 17
        #
        # if money_to_spend is None:
        #     money_to_spend = self.calc_money_to_spend(group)
        # if money_to_get is None:
        #     money_to_get = self.calc_money_to_get(group)
        #
        # return [player_info, others_info, self.norm_money(self.money),
        #         self.norm_money(money_to_spend), self.norm_money(money_to_get)]



# class State:
#     def __init__(self, player, game):
#         self.game = game
#         self.player_info = [0] * len(game.groups)
#         self.others_info = [0] * len(game.groups)
#
#         for i in range(len(game.groups)):
#             group = game.groups[i]
#             if group.owner() is None:
#                 group_props = [prop for prop in group.properties if prop.has_owner() and not prop.mortgaged]
#                 player_props = len([prop for prop in group_props if prop.owner is player])
#                 others_props = len(group_props) - player_props
#                 x = 12 / group.num_props()
#                 self.player_info[i] = x * player_props / 17
#                 self.others_info[i] = x * others_props / 17
#             else:
#                 owner = group.owner()
#                 max_buildings = max([prop.buildings for prop in group.properties])
#                 if owner is player:
#                     self.player_info[i] = (12 + max_buildings) / 17
#                 else:
#                     self.others_info[i] = (12 + max_buildings) / 17
#
#         player_props = 0
#         total_props = 0.001
#         for card in game.board:
#             if card.is_property and card.has_owner():
#                 if card.owner is player:
#                     player_props += 1
#                 total_props += 1
#
#         self.relative_props = player_props / total_props
#         self.money = player.money
#
#     def normalize_money(self):
#         return self.game.smooth_function((self.money / MAX_MONEY))
#
#     def get_state(self, group):
#         pos = (1 + self.game.groups.index(group)) / len(self.game.groups)
#         return self.player_info + self.others_info + [pos, self.relative_props, self.normalize_money()]
#
#     def get_state_taking_money(self, amount, group):
#         self.money -= amount
#         return self.get_state(group)
