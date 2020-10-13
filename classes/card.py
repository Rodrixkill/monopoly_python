class Group:
    def __init__(self, color, properties, building_cost, is_color=True):
        self.color = color
        self.properties = properties
        self.building_cost = building_cost
        self.is_color = is_color
        for prop in self.properties:
            prop.group = self

    def owner(self):
        owner = self.properties[0].owner
        mortgaged = any([card.mortgaged for card in self.properties])
        same_owner = all([card.owner is owner for card in self.properties])
        if not mortgaged and same_owner:
            return owner
        return None

    def num_props(self):
        return len(self.properties)

    def num_owned(self, owner):
        return len([prop for prop in self.properties if prop.owner is owner])

    def has_buildings(self):
        return any([prop.buildings > 0 for prop in self.properties])


class Card:
    def __init__(self, name, is_property=False, is_chance=False,
                 is_community=False, is_go_jail=False, is_special=False,
                 is_tax=False):
        self.name = name
        self.is_property = is_property
        self.is_chance = is_chance
        self.is_community = is_community
        self.is_go_jail = is_go_jail
        self.is_special = is_special
        self.is_tax = is_tax

    def desc(self):
        return self.name


class PropertyCard(Card):
    def __init__(self, name, cost, rent_prices, mortgage_cost):
        Card.__init__(self, name, is_property=True)
        self.group = None
        self.cost = cost
        self.rent_prices = rent_prices
        self.mortgage_cost = mortgage_cost
        self.buildings = 0
        self.owner = None
        self.mortgaged = False

    def desc(self):
        return "%s(%s)" % (self.name, self.group.color)

    def calc_rent(self, dices=None):
        if self.buildings == 0 and self.group.owner() is self.owner:
            return self.rent_prices[0] * 2
        if self.buildings > 5:
            print(self.buildings)
        return self.rent_prices[self.buildings]

    def has_owner(self):
        return self.owner is not None


class RailRoadCard(PropertyCard):
    def __init__(self, name):
        PropertyCard.__init__(self, name, 200, None, 100)

    def calc_rent(self, dices=None):
        num = self.group.num_owned(self.owner)
        return 25 * (2 ** (num-1))


class UtilityCard(PropertyCard):
    def __init__(self, name):
        PropertyCard.__init__(self, name, 150, None, 75)

    def calc_rent(self, dices=None):
        num = self.group.num_owned(self.owner)
        return dices * 10 if num == 2 else dices*4


class TaxCard(Card):
    def __init__(self, name, tax):
        Card.__init__(self, name, is_tax=True)
        self.tax = tax

