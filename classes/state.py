MAX_MONEY = 1500
MAX_POSITION = 40


class State:
    def __init__(self, player, game):
        self.game = game
        self.player_info = [0] * len(game.groups)
        self.others_info = [0] * len(game.groups)

        for i in range(len(game.groups)):
            group = game.groups[i]
            if group.owner() is None:
                group_props = [prop for prop in group.properties if prop.has_owner() and not prop.mortgaged]
                player_props = len([prop for prop in group_props if prop.owner is player])
                others_props = len(group_props) - player_props
                x = 12 / group.num_props()
                self.player_info[i] = x * player_props / 17
                self.others_info[i] = x * others_props / 17
            else:
                owner = group.owner()
                max_buildings = max([prop.buildings for prop in group.properties])
                if owner is player:
                    self.player_info[i] = (12 + max_buildings) / 17
                else:
                    self.others_info[i] = (12 + max_buildings) / 17

        player_props = 0
        total_props = 0.001
        for card in game.board:
            if card.is_property and card.has_owner():
                if card.owner is player:
                    player_props += 1
                total_props += 1

        self.finance = [player_props / total_props, game.smooth_function(player.money / MAX_MONEY)]

    def get_state(self, group):
        pos = (1 + self.game.groups.index(group)) / len(self.game.groups)
        return self.player_info + self.others_info + [pos] + self.finance