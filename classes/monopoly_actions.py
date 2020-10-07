class Actions:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def buy_property(self, player, prop):
        if prop.is_property and not prop.has_owner() and prop.owner is not player and player.money > prop.cost:
            prop.owner = player
            player.money -= prop.cost
            player.properties.append(prop)
            if self.verbose:
                print("%s buys property %s for %d$" % (player.name, prop.desc(), prop.cost))
                print("%s's new balance: %d$" % (player.name, player.money))
            return True
        return False

    def unmortgage_property(self, player, prop):
        if prop.is_property and prop.owner is player and prop.mortgaged and player.money > prop.mortgage_cost * 1.1:
            prop.mortgaged = False
            player.money -= prop.mortgage_cost * 1.1
            if self.verbose:
                print("%s unmortgages property %s for %d$" % (player.name, prop.desc(), prop.mortgage_cost * 1.1))
                print("%s's new balance: %d$" % (player.name, player.money))
            return True
        return False

    def build_on_area(self, player, group, game):
        if group.is_color and group.owner() is player and player.money > group.building_cost:
            props = sorted(group.properties, key=lambda x: x.houses)
            prop_to_build = props[0]
            if prop_to_build.buildings < 4 and game.houses > 0:
                game.houses -= 1
                prop_to_build.buildings += 1
                player.money -= group.building_cost
                if self.verbose:
                    print("%s builds a house on %s for %d$" % (player.name, prop_to_build.desc(), group.building_cost))
                    print("%s's new balance: %d$" % (player.name, player.money))
                return True
            elif prop_to_build.buildings == 4 and game.hotels > 0:
                game.hotels -= 1
                game.houses += 4
                prop_to_build.buildings += 1
                player.money -= group.building_cost
                if self.verbose:
                    print("%s builds a hotel on %s for %d$" % (player.name, prop_to_build.desc(), group.building_cost))
                    print("%s's new balance: %d$" % (player.name, player.money))
                return True
        return False

    def mortgage_property(self, player, prop):
        if prop.is_property and prop.owner is player and not prop.group.has_buildings() and not prop.mortgaged:
            prop.mortgaged = True
            player.money += prop.mortgage_cost
            if self.verbose:
                print("%s mortgages %s for %d$" % (player.name, prop.desc(), prop.mortgage_cost))
                print("%s's new balance: %d$" % (player.name, player.money))
            return True
        return False

    def sell_on_area(self, player, group, game):
        if group.is_color and group.owner() is player:
            props = sorted(group.properties, key=lambda x: x.houses, reverse=True)
            prop_to_sell = props[0]
            if 0 < prop_to_sell.buildings < 5:
                game.houses += 1
                prop_to_sell.buildings -= 1
                player.money += 0.5 * group.building_cost
                if self.verbose:
                    print("%s sells house of %s for %d$" % (player.name, prop_to_sell.desc(), group.building_cost * 0.5))
                    print("%s's new balance: %d$" % (player.name, player.money))
                return True
            elif prop_to_sell.buildings == 5 and game.houses >= 4:
                game.hotels += 1
                game.houses -= 4
                prop_to_sell.buildings -= 1
                player.money += 0.5 * group.building_cost
                if self.verbose:
                    print("%s sells hotel of %s for %d$" % (player.name, prop_to_sell.desc(), group.building_cost * 0.5))
                    print("%s's new balance: %d$" % (player.name, player.money))
                return True
        return False

    def pay_money(self, amount, player, target, game):
        if player.money < amount:
            can_sell = True
            while player.money < amount and can_sell:
                can_sell = self.sell_property(player, game)
            if player.money < amount:
                return False

        player.money -= amount
        if self.verbose:
            target_name = "The Bank" if target is None else target.name
            print("%s pays %d$ to %s" % (player.name, amount, target_name))
            print("%s's new balance: %d$" % (player.name, player.money))
        if target is not None:
            target.money += amount
            if self.verbose:
                print("%s's new balance: %d$" % (target.name, target.money))
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



















