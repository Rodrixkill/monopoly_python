class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.properties = []
        self.current_pos = 0
        self.in_jail = False
        self.turns_in_jail = 0
        self.bankrupt = False

    def reset(self):
        self.properties = []
        self.money = 1500
        self.current_pos = 0
        self.in_jail = False
        self.turns_in_jail = 0
        self.bankrupt = False

    def total_net_worth(self):
        net_worth = self.money
        for prop in self.properties:
            net_worth += prop.mortgage_cost
            net_worth += prop.buildings*prop.group.building_cost*0.5
        return net_worth
