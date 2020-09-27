class CommunityChest:
    def __init__(self, card_name, type, movement, pay, receive, destination, money):
        self.card_name = card_name      # str
        self.type = type                # str
        self.movement = movement        # bool
        self.pay = pay                  # bool
        self.receive = receive          # bool
        self.destination = destination  # int
        self.money = money              # int