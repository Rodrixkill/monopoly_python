"""
Contains the Player class and associated functions.
"""
import random
from classes import card_definitions as c_def


class Player:
    def __init__(self, name):
        self.name = name                # str
        self.balance = 1500             # int
        self.cards_owned = []           # list
        self.current_pos = 0            # int (index)
        self.in_jail = False            # bool
        self.railroads_owned = 0        # int
        self.doubles_counter = 0        # int
        self.amount_owed = 0            # int
        self.bankruptcy_status = False  # bool

    def roll_dice(self):
        """
        Simulates the randomness of throwing two die.
        :return: n: an int between 2 and 12 inclusive.
        """
        random.seed()
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        if dice1 == dice2:
            self.doubles_counter+=1
        n = dice1 + dice2
        return n

    def move_player(self, dice_amt):
        """
        Moves the player by the amount returned by rolling two die.
        :param dice_amt: int, the number rolled by the two die.
        :return: an int that represents the updated position of the player on the board.
        """
        self.current_pos += dice_amt
        return self.current_pos

    def check_pos(self, board): # TODO
        """
        Checks what card the player has landed on and carries out the appropriate action.
        :param board: list, the monopoly board.
        :return: None
        """
        self.current_pos = self.current_pos % 40
        brd_property = board[self.current_pos]

        if brd_property.card_cost == "N/A":  # this means the player cannot purchase the card

            if brd_property.card_name == 'Jail/Visiting Jail':
                print(f"{self.name} is visiting jail.")

            elif brd_property.card_name == 'Luxury Tax':
                print(f"{self.name} landed on Luxury Tax and has been fined $75")
                self.reduce_balance(75)

            elif brd_property.card_name == 'Income Tax':
                print(f"{self.name} landed on Income Tax and has been fined $200")
                self.reduce_balance(200)

            elif brd_property.card_name == 'Go to Jail':
                print(f"{self.name} landed on Go to Jail and has been arrested!")
                self.send_to_jail()

            else:
                print(f"{self.name} landed on {brd_property.card_name}")

        else:
            if brd_property.mortgaged:
                print(f"{self.name} landed on a mortgaged property.")

            elif brd_property.owner != 'Bank':  # and brd_property.owner.name != self.name:
                if brd_property.owner.name == self.name:
                    print(f"{self.name} landed on {brd_property.card_name}, a property they own.")
                else:
                    print(
                        f"{self.name} landed on {brd_property.card_name}, a property owned by {brd_property.owner.name}")
                    self.charge_rent(brd_property)

            else:
                print(f"{self.name} landed on {brd_property.card_name}")
                if self.name == "AI":
                    return 1  # Indicates to the AI that the property can be purchased
                else:
                    user_action = input("Do you want to buy the property? (y/n) ")
                    if user_action == 'y':
                        brd_property.purchase_card(self)

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
        if card.color_group == "Railroad":
            rent_amt = 25 * card.owner.railroads_owned
        elif card.mortgaged == False:
            total_casas=card.houses_built
            rent_amt = card.rent_prices[total_casas]
        self.reduce_balance(rent_amt)
        card.owner.add_balance(rent_amt)

    def reduce_balance(self, amount): #TODO
        """
        Reduces the player's balance.
        :param amount: int, the amount of money to reduce the player's balance by.
        :return: None.
        """
        if self.balance < amount:
            print("Your balance is insufficient for this action.")
            bankrupt = self.check_if_bankrupt(amount)
            if not bankrupt:
                print("You need to sell or mortgage certain properties.")
                user_action = input("Do you want to sell or mortgage? (s/m)")
                if user_action == 's':
                    pass  # sell()  TODO: implement this function.
                else:
                    pass  # mortgage()  TODO: implement this function.
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

        self.bankruptcy_status = True

    def bankrupt_player_to_player(self,player):
        """
        The designed player collects all the player's owned properties and sets their bankruptcy status to True.
        :return: None.
        """
        self.balance = 0

        if len(self.cards_owned):
            for card in self.cards_owned:
                card.owner = player.name
        self.railroads_owned = 0

        self.bankruptcy_status = True

    def check_if_bankrupt(self, amt_owed): #TODO
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
            print(f"Unfortunately, {self.name} is now bankrupt! It's game over for them!")
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

    def player_action(self, user_choice, player_list, computer, board):
        """
        Takes in the user's choice of what action to take and carries out that action.
        :param user_choice: char, what the player chooses to do (e.g. r to roll the dice).
        :return: None.
        """
        # TODO: add sell, mortgage, and construct house functions.
        val = -1
        if user_choice == "r":
            val = self.roll_dice()
        elif user_choice == "b":
            print(f"Your balance is: ${self.balance}")
        elif user_choice == "c":
            print("Your properties are:")
            self.display_player_properties()
        elif user_choice == "s":
            print("Sell property feature coming soon.")
        elif user_choice == "m":
            print("Mortgage property feature coming soon.")
        elif user_choice == "h":
            print("Construct house feature coming soon.")
        elif user_choice == "t":
            self.trade_with_ai(computer, board)
        elif user_choice == "p":
            trading_partner = input("Enter the name of the player you're trading with. ")
            self.trade_with_human(trading_partner, player_list, board)
        else:
            print("Please enter a valid command.")

        return val

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
        self.doubles_counter = 0
        self.roll_dice()
        if self.doubles_counter == 1:
            self.doubles_counter = 0
            self.in_jail = False
            dice_result = self.roll_dice()
            self.move_player(dice_result)

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