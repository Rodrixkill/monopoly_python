from classes import fortune_definitions as c_def


# def __init__(self, card_name, type, movement, pay, receive, destination, money):
def initialize_community_cards():
    # receive
    collect_gift = c_def.Fortune("It's your bithday", "Collect $10 from every player", False, False,
                                 False, 0, 10)
    receive_consultancy = c_def.Fortune("Consultancy fee", "Receive $25", False, False, True, 0, 25)
    receive_fund = c_def.Fortune("Holiday", "Receive $100", False, False, True, 0, 100)
    receive_insurance = c_def.Fortune("Life insurance", "Collect $100", False, False, True, 0, 100)
    receive_tax = c_def.Fortune("Refund tax", "Collect $20", False, False, True, 0, 20)
    receive_errorbank = c_def.Fortune("Bank error", "You get $200", False, False, True, 0, 200)
    receive_inherit = c_def.Fortune("You inherit", "Receive $100", False, False, True, 0, 100)
    receive_prize = c_def.Fortune("Won a contest", "Collect $10", False, False, True, 0, 10)

    # pay
    fee_school = c_def.Fortune("School fees", "Pay $150", False, True, False, 0, 150)
    fee_hospital = c_def.Fortune("Hospital fees", "Pay $100", False, True, False, 0, 100)
    street_repairs = c_def.Fortune("Street repairs", "Pay $40 per house and $115 per hotel you own", False,
                                   False, False, 0, 40)
    fee_doctor = c_def.Fortune("Doctor's fees", "Pay $50", False, True, False, 0, 50)

    # move
    go_jail = c_def.Fortune("Go to jail", "Directly to jail", True, False, False, 10, 0)
    out_jail = c_def.Fortune("Free of jail", "This card may be kept until needed or sold/traded.", False,
                             False, False, 0, 0)
    go_go = c_def.Fortune("Advance to Go", "Collect $200", True, False, False, 0, 0)

    community = [
        fee_school,
        collect_gift,
        receive_consultancy,
        receive_fund,
        go_jail,
        fee_hospital,
        receive_insurance,
        receive_tax,
        out_jail,
        receive_errorbank,
        go_go,
        receive_inherit,
        street_repairs,
        receive_prize,
        fee_doctor
    ]

    return community
