
class Fortune:
    def __init__(self, card_name, type,movement,pay,receive,destination,money):
        self.card_name = card_name                  # str
        self.type = type                            # str
        self.movement= movement                     # bool
        self.pay=pay                                # bool
        self.receive=receive                        # bool
        self.destination=destination                # int
        self.money=money                            # int

    def play(self,player,otherplayers):
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
            player.send_to_jail()
