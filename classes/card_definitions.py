
class Card:
    def __init__(self, card_name, color_group, card_cost, house_cost, houses_built, rent_prices, mortgage_amt, owner, mortgaged):
        self.card_name = card_name                  # str
        self.color_group = color_group              # str
        self.card_cost = card_cost                  # int
        self.house_cost = house_cost                # int
        self.houses_built = houses_built            # int
        self.rent_prices = rent_prices              # int
        self.mortgage_amt = mortgage_amt            # int
        self.owner = owner                          # str
        self.mortgaged = mortgaged                  # bool

    def mortgage(self, player):
        """
        Sets the card's mortgaged status to True and updates the player's balance.
        :param player: An instance of the Player class.
        """
        player.add_balance(self.mortgage_amt)
        self.mortgaged = True

    def buy_mortgage(self, player):
        """
        Set Mortgage to false and pay the mortgage price plus 10%
        :param player: An instance of the Player class.
        :returns: Assert Error if not completed correctly.
        """
        mortgage_cost = self.mortgage_amt * 1.10
        assert player.balance >= mortgage_cost
        player.reduce_balance(mortgage_cost)
        self.mortgaged = False

    def sell(self, player):
        """
        Returns ownership of the card to the Bank and updates the player's balance.
        :param player: An instance of the Player class.
        :returns: Assert Error if not completed correctly.
        """
        player.add_balance(self.card_cost)
        self.owner = 'Bank'

    def has_owner(self, player):
        return self.owner is not 'Bank'

    def sell_player(self, player, player2, cost):
        """
        Returns ownership of the card to the Bank and updates the player's balance.
        :param player: An instance of the Player class.
        :return: 1.
        """
        player.add_balance(cost)
        player2.reduce_balance(cost)
        self.owner = player2.name

    def sell_house(self, player):
        """
        Returns ownership of the card to the Bank and updates the player's balance.
        :param player: An instance of the Player class.
        :returns: Assert Error if not completed correctly.
        """
        assert self.houses_built > 0
        house_sell_value=self.house_cost/2
        player.add_balance(house_sell_value)
        self.houses_built -= 1

    def purchase_card(self, player):
        """
        Gives ownership of the card to the Bank and updates the player's balance.
        :param player: An instance of the Player class.
        :returns: Assert Error if not completed correctly.
        """
        assert self.card_cost <= player.balance
        player.cards_owned.append(self)
        player.reduce_balance(self.card_cost)
        self.owner = player

    def construct_house(self, player):
        """
        Updates number of houses that have been built on the card.
        :param player: An instance of the Player class.
        """
        assert self.house_cost <= player.balance or self.houses_built < 5
        player.balance = player.balance - self.house_cost
        self.houses_built += 1

    def __str__(self):
        return '%s(%s)' % (self.card_name, self.color_group)



def locate_card_object(name, board):

    for card in board:
        if card.card_name == name:
            card_object = card
            break

    return card_object
