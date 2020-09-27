from classes import communitychest_definitions as c_def


# def __init__(self, card_name, type, movement, pay, receive, destination, money):
def initialize_community_cards():
    fee_school = c_def.CommunityChest("School fees", "Pay $150", False, True, False, 0, 150)
    collect_gift = c_def.CommunityChest("It's your bithday", "Collect $10 from every player", False, False,
                                        True, 0, 10)
    receive_consultancy = c_def.CommunityChest("Consultancy fee", "Receive $25", False, False, True, 0, 25)
    receive_fund = c_def.CommunityChest("Holiday", "Receive $100", False, False, True, 0, 100)
    go_jail = c_def.CommunityChest("Go to jail", "Directly to jail", True, False, False, 10, 0)
    fee_hospital = c_def.CommunityChest("Hospital fees", "Pay $100", False, True, False, 0, 100)
    receive_insurance = c_def.CommunityChest("Life insurance", "Collect $100", False, False, True, 0, 100)
    receive_tax = c_def.CommunityChest("Refund tax", "Collect $20", False, False, True, 0, 20)
    out_jail = c_def.CommunityChest("Free of jail", "This card may be kept until needed or sold/traded.", True,
                                    False, False, 0, 0)
    receive_errorbank = c_def.CommunityChest("Bank error", "You get $200", False, False, True, 0, 200)
    go_go = c_def.CommunityChest("Advance to Go", "Collect $200", True, False, True, 0, 200)
    receive_inherit = c_def.CommunityChest("You inherit", "Receive $100", False, False, True, 0, 100)
    street_repairs = c_def.CommunityChest("Street repairs", "Pay $40 per house and $115 per hotel you own", False,
                                          True, False, 0, 40)
    receive_prize = c_def.CommunityChest("Won a contest", "Collect $10", False, False, True, 0, 10)
    fee_doctor = c_def.CommunityChest("Doctor's fees", "Pay $50", False, True, False, 0, 50)

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
