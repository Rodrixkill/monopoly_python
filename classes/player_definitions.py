"""
Contains the Player class and associated functions.
"""
import random
from typing import List

from classes import card_definitions as c_def
from classes.card_definitions import  Card
import classes.actions as acts



class Player:
    def __init__(self, name):
        self.name = name  # str
        self.balance = 1500  # int
        self.cards_owned: List[Card] = []  # list
        self.current_pos = 0  # int (index)
        self.in_jail = False  # bool
        self.railroads_owned = 0  # int
        self.utilities_owned = 0  # int
        self.doubles_counter = 0  #int
        self.amount_owed = 0  # int
        self.bankruptcy = False  # bool
        self.turns_in_jail = 0        #int
        #TODO
        self.properties_by_color = {
            "Orange": [],
            "Pink": []
        }
        self.dice1= 0 # int
        self.dice2= 0 # int
        self.brown = 0  # int
        self.lightblue = 0  # int
        self.pink = 0  # int
        self.orange = 0  # int
        self.red = 0  # int
        self.yellow = 0  # int
        self.green = 0  # int
        self.blue = 0  # int

    def reset(self):
        pass #TODO

    def roll_dice(self):
        """
        Simulates the randomness of throwing two die.
        :return: n: an int between 2 and 12 inclusive.
        """
        random.seed()
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.dice1=dice1
        self.dice2=dice2
        return dice1, dice2

    def move_player(self, dice_amt):
        """
        Moves the player by the amount returned by rolling two die.
        :param dice_amt: int, the number rolled by the two die.
        :return: an int that represents the updated position of the player on the board.
        """
        self.current_pos += dice_amt
        self.current_pos = self.current_pos % 40
        return self.current_pos

    def move_player_card(self, destination):
        """
        Moves the player by the amount returned by rolling two die.
        :param dice_amt: int, the number rolled by the two die.
        :return: an int that represents the updated position of the player on the board.
        """
        self.current_pos = destination
        return self.current_pos

    def buy_property(self, card):
        """
        Buy card to make it your property
        :param card:
        :return:
        """
        assert card.owner == 'Bank'
        assert card.card_cost <= self.balance

        if card.card_cost <= self.balance:
            card.owner = self.name
            self.reduce_balance(card.card_cost)
            if card.color_group == "Railroad":
                self.railroads_owned += 1
            elif card.color_group == "Utilities":
                self.utilities_owned += 1
            elif card.color_group == "Brown":
                self.brown += 1
            elif card.color_group == "Light Blue":
                self.lightblue += 1
            elif card.color_group == "Pink":
                self.pink += 1
            elif card.color_group == "Orange":
                self.orange += 1
            elif card.color_group == "Red":
                self.red += 1
            elif card.color_group == "Yellow":
                self.yellow += 1
            elif card.color_group == "Green":
                self.green += 1
            elif card.color_group == "Blue":
                self.blue += 1

    def buy_house(self):
        pass
        #TODO se compra por color y se asigna parejamente a cada propiedad

    def buy_property_to_price(self, card, money):
        """
        Buy card to make it your property
        :param card:
        :return:
        """
        assert card.owner == 'Bank'
        if card.card_cost <= self.balance:
            card.owner = self.name
            self.reduce_balance(money)
            if card.color_group == "Railroad":
                self.railroads_owned += 1
            elif card.color_group == "Utilities":
                self.utilities_owned += 1
            elif card.color_group == "Brown":
                self.brown += 1
            elif card.color_group == "Light Blue":
                self.lightblue += 1
            elif card.color_group == "Pink":
                self.pink += 1
            elif card.color_group == "Orange":
                self.orange += 1
            elif card.color_group == "Red":
                self.red += 1
            elif card.color_group == "Yellow":
                self.yellow += 1
            elif card.color_group == "Green":
                self.green += 1
            elif card.color_group == "Blue":
                self.blue += 1

    def check_pos(self, board):
        """
        Checks what card the player has landed on and carries out the appropriate action.
        :param board: list, the monopoly board.
        :return: None
        """
        self.current_pos = self.current_pos % 40
        brd_property = board[self.current_pos]
        if brd_property.owner == 'Bank':
            # TODO buy or not buy
            return 0
        else:  # and brd_property.owner.name != self.name:
            if brd_property.owner.name != self.name:
                self.charge_rent(brd_property)

    def add_balance(self, amount):
        """
        Increases the player's balance.
        :param amount: int, the amount of money to add to the player's balance.
        :return: self.balance: the updated balance of the player.
        """
        self.balance += amount
        return self.balance

    def charge_rent(self, card):
        """
        Charges the rent cost to the player.
        :param card: an instance of the Card class.
        :return: None.
        """
        rent_amt = 0
        if card.color_group == "Railroad":  # 25,50,100,200
            if card.owner.railroads_owned == 1:
                rent_amt = 25
            elif card.owner.railroads_owned == 2:
                rent_amt = 50
            elif card.owner.railroads_owned == 3:
                rent_amt = 100
            elif card.owner.railroads_owned == 4:
                rent_amt = 200
        elif card.color_group == "Utilities":
            n = self.dice1 + self.dice2
            if card.owner.utilities_owned == 1:
                rent_amt = 4 * n
            elif card.owner.utilities_owned == 2:
                rent_amt = 10 * n
        elif card.mortgaged == False:
            total_houses = card.houses_built
            rent_amt = card.rent_prices[total_houses]
            if total_houses == 0:
                if card.color_group == "Brown" and card.owner.brown == 2:
                    rent_amt *= 2
                elif card.color_group == "Light Blue" and card.owner.lightblue == 3:
                    rent_amt *= 2
                elif card.color_group == "Pink" and card.owner.pink == 3:
                    rent_amt *= 2
                elif card.color_group == "Orange" and card.owner.orange == 3:
                    rent_amt *= 2
                elif card.color_group == "Red" and card.owner.red == 3:
                    rent_amt *= 2
                elif card.color_group == "Yellow" and card.owner.yellow == 3:
                    rent_amt *= 2
                elif card.color_group == "Green" and card.owner.green == 3:
                    rent_amt *= 2
                elif card.color_group == "Blue" and card.owner.blue == 2:
                    rent_amt *= 2
        self.reduce_balance(rent_amt)
        card.owner.add_balance(rent_amt)

    def reduce_balance(self, amount):  # TODO
        """
        Reduces the player's balance.
        :param amount: int, the amount of money to reduce the player's balance by.
        :return: None.
        """
        if self.balance < amount:
            """
            print("Your balance is insufficient for this action.")
            bankrupt = self.check_if_bankrupt(amount)
            if not bankrupt:
                print("You need to sell or mortgage certain properties.")
                user_action = input("Do you want to sell or mortgage? (s/m)")
                if user_action == 's':
                    pass  # sell()  TODO: implement this function.
                else:
                    pass  # mortgage()  TODO: implement this function.
            """
        else:
            self.balance -= amount

    def bankrupt_player_to_bank(self):
        """
        Bank collects all the player's owned properties and sets their bankruptcy status to True.
        :return: None.
        """
        self.balance = 0

        if len(self.cards_owned):
            for card in self.cards_owned:
                card.owner = "Bank"
        self.railroads_owned = 0

        self.bankruptcy = True

    def bankrupt_player_to_player(self, player):
        """
        The designed player collects all the player's owned properties and sets their bankruptcy status to True.
        :return: None.
        """
        self.balance = 0

        if len(self.cards_owned):
            for card in self.cards_owned:
                card.owner = player.name
                if card.color_group == "Railroad":
                    player.railroads_owned += 1
                elif card.color_group == "Utilities":
                    player.utilities_owned += 1
                elif card.color_group == "Brown":
                    player.brown += 1
                elif card.color_group == "Light Blue":
                    player.lightblue += 1
                elif card.color_group == "Pink":
                    player.pink += 1
                elif card.color_group == "Orange":
                    player.orange += 1
                elif card.color_group == "Red":
                    player.red += 1
                elif card.color_group == "Yellow":
                    player.yellow += 1
                elif card.color_group == "Green":
                    player.green += 1
                elif card.color_group == "Blue":
                    player.blue += 1
        self.bankruptcy = True

    def check_if_bankrupt(self, amt_owed):  # TODO
        """
        Checks if the player is bankrupt (i.e. can the player afford what they are being charged?).
        :param amt_owed: int, the amount the player is being charged.
        :return: Bool that represents if the player is bankrupt or not.
        """
        net_worth = 0

        for card in self.cards_owned:
            if card.mortgaged:
                net_worth -= card.mortgage_amt
                net_worth += card.card_cost
            else:
                net_worth += card.card_cost

        if (self.balance + net_worth) < amt_owed:
            self.bankrupt_player()
            return True
        else:
            return False

    def display_player_properties(self):
        """
        Prints out all the cards the player owns.
        :return: None.
        """
        total = 0
        for card in self.cards_owned:
            print(f"{card.card_name}: ${card.card_cost}")
            total += card.card_cost
        print(f"The sum of your card costs is: ${total}")

    def send_to_jail(self):
        """
        Sends the player to jail.
        :return: None.
        """
        self.current_pos = 10
        self.doubles_counter = 0
        self.in_jail = True

    def release_from_jail_by_rolling(self):
        """
        Releases the player from jail.
        :return: None.
        """
        self.roll_dice()
        if self.turns_in_jail == 3:
            self.release_from_jail_paying()
        elif self.dice1 == self.dice2:
            self.doubles_counter = 0
            self.in_jail = False
            dice_result = self.roll_dice()
            self.move_player(dice_result)
        else:
            self.turns_in_jail+=1

    def release_from_jail_paying(self):
        """
        Releases the player from jail.
        :return: None.
        """
        self.doubles_counter = 0
        self.reduce_balance(50)
        self.in_jail = False
        dice_result = self.roll_dice()
        self.move_player(dice_result)

    def trade_between_players(self, player2, listP1, listP2, m1, m2):
        """
        Trade Between players giving themselves properties or money
        :param player2:
        :param listP1:
        :param listP2:
        :param m1:
        :param m2:
        :return:
        """
        self.reduce_balance(m1)
        player2.reduce_balance(m2)
        self.add_balance(m2)
        player2.add_balance(m1)
        if len(listP1):
            for card in listP1:
                card.owner = player2.name
                if card.color_group == "Railroad":
                    player2.railroads_owned += 1
                    self.railroads_owned -= 1
                elif card.color_group == "Utilities":
                    player2.utilities_owned += 1
                    self.utilities_owned -= 1
                elif card.color_group == "Brown":
                    player2.brown += 1
                    self.brown -= 1
                elif card.color_group == "Light Blue":
                    player2.lightblue += 1
                    self.lightblue -= 1
                elif card.color_group == "Pink":
                    player2.pink += 1
                    self.pink -= 1
                elif card.color_group == "Orange":
                    player2.orange += 1
                    self.orange -= 1
                elif card.color_group == "Red":
                    player2.red += 1
                    self.red -= 1
                elif card.color_group == "Yellow":
                    player2.yellow += 1
                    self.yellow -= 1
                elif card.color_group == "Green":
                    player2.green += 1
                    self.green -= 1
                elif card.color_group == "Blue":
                    player2.blue += 1
                    self.blue -= 1
        if len(listP2):
            for card in listP2:
                card.owner = self.name
                if card.color_group == "Railroad":
                    player2.railroads_owned -= 1
                    self.railroads_owned += 1
                elif card.color_group == "Utilities":
                    player2.utilities_owned -= 1
                    self.utilities_owned += 1
                elif card.color_group == "Brown":
                    player2.brown -= 1
                    self.brown += 1
                elif card.color_group == "Light Blue":
                    player2.lightblue -= 1
                    self.lightblue += 1
                elif card.color_group == "Pink":
                    player2.pink -= 1
                    self.pink += 1
                elif card.color_group == "Orange":
                    player2.orange -= 1
                    self.orange += 1
                elif card.color_group == "Red":
                    player2.red -= 1
                    self.red += 1
                elif card.color_group == "Yellow":
                    player2.yellow -= 1
                    self.yellow += 1
                elif card.color_group == "Green":
                    player2.green -= 1
                    self.green += 1
                elif card.color_group == "Blue":
                    player2.blue -= 1
                    self.blue += 1

    def total_net_worth(self):
        net_worth=self.balance
        for card in self.cards_owned:
            net_worth+=(card.card_cost/2)
            net_worth+=(card.houses_built*card.house_cost)/2
        return net_worth

    def V(self, state):
        return random.random() * 2 - 1

    def take_action(self, actions):
        value_action_pairs = [(self.V(action.peek_state()), action) for action in actions]
        value_action_pairs.sort(key=lambda x: x[0], reverse=True)
        return value_action_pairs[0][1]

    def want_to_bid(self, prop, actual_bid):
        #TODO peek posible state
        posible_state, actual_state = None, None
        return self.V(posible_state) > self.V(actual_state)
