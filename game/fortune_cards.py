from classes import fortune_definitions as f_def


# def __init__(self, card_name, type, movement, pay, receive, destination, money):
def initialize_fortune_cards():
    go_boardwalk = f_def.Fortune("Go BoardWalk", "Advance to boardwalk", True, False, False, 39, 0)

    go_reading_rr = f_def.Fortune("Trip Railroad Reading", "Go Railroad Reading, If you pass Go, collect $200", True,
                                  False, False, 5, 0)

    loan_matures = f_def.Fortune("Loan Matures", "Building and loan matures receive $150", False, False, True, 0, 150)

    go_illinois = f_def.Fortune("Advance to Illinois Ave", "Go to Illinois Ave, If you pass Go, collect $200",
                                True, False, False, 24, 0)

    near_utility = f_def.Fortune("Advance to nearest utility",
                                 "If unowned, you can buy it. If owned, throw dice and pay 10 times the amount thrown",
                                 True, False, False, 12 | 28, 0)

    out_jail = f_def.Fortune("Get out of jail", "This card may be kept until needed, or traded/sold", True, False,
                             False, 0, 0)

    pay_all = f_def.Fortune("Chairman of the Board", "Pay each player $50", False, True, False, 0, 50)

    bank_pay = f_def.Fortune("Bank pays you", "Dividend of $50", False, False, True, 0, 50)

    repairs = f_def.Fortune("Make repairs", "For each house pay $25, For each hotel $100.", False, True, False, 0, 0)

    go_charles = f_def.Fortune("Advance to Charles Place", "Go to Charles Place, If you pass Go, collect $200.",
                               True, False, False, 11, 0)

    go_jail = f_def.Fortune("Go to jail", "Directly to jail", True, False, False, 10, 0)

    won_competition = f_def.Fortune("Won a competition", "Collect $100", False, False, True, 0, 100)

    back_three = f_def.Fortune("Go Back", "Back 3 spaces", True, False, False, -3, 0)

    near_railroad = f_def.Fortune("Advance to nearest railroad",
                                  "If unowned, you can buy it. If owned, pay owner twice the rental", True, True, False,
                                  5 | 15 | 25, 0)

    pay_tax = f_def.Fortune("Pay tax", "Poor tax of $15", False, True, False, 0, 15)

    go_go = f_def.Fortune("Advance to go", "Collect $100", True, False, True, 0, 200)

    fortune = [
        go_boardwalk,
        go_reading_rr,
        loan_matures,
        go_illinois,
        near_utility,
        out_jail,
        pay_all,
        bank_pay,
        repairs,
        go_charles,
        go_jail,
        won_competition,
        back_three,
        near_railroad,
        pay_tax,
        go_go
    ]

    return fortune