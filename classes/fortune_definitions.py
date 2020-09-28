class Fortune:
    def __init__(self, card_name, type, movement, pay, receive, destination, money):
        self.card_name = card_name      # str
        self.type = type                # str
        self.movement = movement        # bool
        self.pay = pay                  # bool
        self.receive = receive          # bool
        self.destination = destination  # int
        self.money = money              # int

    def play(self, player, otherplayers):
        if self.movement:
            if player.current_pos >= self.destination:
                player.add_balance(200)
            player.move_player_card(self.destination)
        if self.receive:
            player.add_balance(self.money)
        if self.pay:
            player.reduce_balance(self.money)
        if self.card_name == 'Go to Jail':
            player.send_to_jail()
        if self.card_name == 'Pay to all':
            player.reduce_balance(25 * len(otherplayers))
            for p in otherplayers:
                p.add_balance(25)
        elif self.card_name == 'Chairman of the Board':
            player.reduce_balance(50 * len(otherplayers))
            for p in otherplayers:
                p.add_balance(50)
        elif self.card_name == "It's your bithday":
            for p in otherplayers:
                p.reduce_balance(10)
            player.add_balance(10*len(otherplayers))
        elif self.card_name == 'Make repairs':
            for card in player.cards_owned:
                if card.houses_built > 0:
                    if card.houses_built == 5:
                        player.reduce_balance(100)
                    else:
                        player.reduce_balance(25*card.houses_built)
        elif self.card_name == "Street repairs":
            for card in player.cards_owned:
                if card.houses_built > 0:
                    if card.houses_built == 5:
                        player.reduce_balance(115)
                    else:
                        player.reduce_balance(40*card.houses_built)
        elif self.card_name == 'Go Back':
            player.move_player(-3)
        elif self.card_name == 'Advance to nearest railroad' or self.card_name == "Advance to nearest utility":
            val= self.nGE(player.current_pos,self.destination)
            if player.current_pos >= val:
                player.add_balance(200)
            player.move_player_card(val)

    def nGE(val,arr):
        next = min(arr)
        for i in range(len(arr)):
            if arr[i] > val:
                next = arr[i]
                break
        return next