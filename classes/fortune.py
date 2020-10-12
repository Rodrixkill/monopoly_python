class Fortune:
    def __init__(self, name, is_pay=False, is_collect=False, is_pay_buildings=False, is_go_jail=False,
                 is_go_to=False):
        self.name = name
        self.is_pay = is_pay
        self.is_collect = is_collect
        self.is_pay_buildings = is_pay_buildings
        self.is_go_jail = is_go_jail
        self.is_go_to = is_go_to

    def apply(self, game):
        pass


class Pay(Fortune):
    def __init__(self, name, money, to_everyone=False):
        Fortune.__init__(self, name, is_pay=True)
        self.money = money
        self.to_everyone = to_everyone

    def apply(self, game):
        player = game.players[game.player_index]
        if self.to_everyone:
            other_players = [p for p in game.players if p is not player]
            for other_player in other_players:
                game.acts.pay_money(amount=self.money, player=player, target=other_player, game=game)
        else:
            game.acts.pay_money(amount=self.money, player=player, target=None, game=game)


class Collect(Fortune):
    def __init__(self, name, money, from_everyone=False):
        Fortune.__init__(self, name, is_collect=True)
        self.money = money
        self.from_everyone = from_everyone

    def apply(self, game):
        player = game.players[game.player_index]
        if self.from_everyone:
            other_players = [p for p in game.players if p is not player]
            for other_player in other_players:
                game.acts.pay_money(amount=self.money, player=other_player, target=player, game=game)
        else:
            player.money += self.money
            if game.verbose:
                print("%s collects %d from the bank" % (player.name, self.money))


class PayForBuildings(Fortune):
    def __init__(self, name, money_per_house, money_per_hotel):
        Fortune.__init__(self, name, is_pay_buildings=True)
        self.money_per_house = money_per_house
        self.money_per_hotel = money_per_hotel

    def apply(self, game):
        player = game.players[game.player_index]
        buildings_own = [prop.houses for prop in player.properties]
        hotels_own = buildings_own.count(5)
        houses_own = sum(buildings_own) - 5 * hotels_own
        amount = houses_own * self.money_per_house + hotels_own * self.money_per_hotel
        game.acts.pay_money(amount=amount, player=player, target=None, game=game)


class GoJail(Fortune):
    def __init__(self, name):
        Fortune.__init__(self, name, is_go_jail=True)

    def apply(self, game):
        player = game.players[game.player_index]
        game.acts.send_to_jail(player)


class GoTo(Fortune):
    def __init__(self, name, dest=None, num=0):
        Fortune.__init__(self, name, is_go_to=True)
        self.dest = dest
        self.num = num

    def apply(self, game):
        player = game.players[game.player_index]
        if self.num != 0:
            dest = (player.current_pos + self.num) % 40
        else:
            dest = self.dest
        game.acts.move_player(player, position=dest)
        game.acts.check_pos(player, game)


class GoToNearest(Fortune):
    def __init__(self, name, places, mult=1):
        Fortune.__init__(self, name, is_go_to=True)
        self.places = sorted(places)
        self.mult = mult

    def get_nearest(self, game):
        player = game.players[game.player_index]
        higher_position = [x for x in self.places if x > player.current_pos]
        if len(higher_position) == 0:
            dest = self.places[0]
        else:
            dest = higher_position[0]
        return dest


class GoToNearestUtility(GoToNearest):
    def apply(self, game):
        player = game.players[game.player_index]
        dest = self.get_nearest(game)
        game.acts.move_player(player, position=dest)
        utility = game.board[dest]
        if utility.has_owner() and utility.owner is not player:
            dice1, dice2 = game.acts.roll_dices()
            game.acts.pay_money(self.mult*(dice1+dice2), player, utility.owner, self)


class GoToNearestRailroad(GoToNearest):

    def apply(self, game):
        player = game.players[game.player_index]
        dest = self.get_nearest(game)
        game.acts.move_player(player, position=dest)
        railroad = game.board[dest]
        if railroad.has_owner() and railroad.owner is not player:
            game.acts.pay_money(self.mult*(railroad.calc_rent()), player, railroad.owner, self)
