from classes.fortune import Pay, Collect, PayForBuildings, GoJail, GoTo, GoToNearestUtility, GoToNearestRailroad
import random


def initialize_community_cards():
    cards = [
        GoTo("Advance to Go. Collect $200.", dest=0),
        Collect("Bank error. You get $200.", 200),
        Pay("Doctor's fees. Pay $50.", money=50),
        Collect("From sale of stock you get $50.", money=50),
        GoJail("Go directly to jail. Do not pass Go, Do not collect $200."),
        Collect("Grand Opera Night. Collect $50 from every player for opening night seats.", money=50,
                from_everyone=True),
        Collect("Holiday Fund matures. Receive $100.", money=100),
        Collect("Income tax refund. Collect $20", money=20),
        Collect("It's your birthday. Collect $10 from every player.", money=10, from_everyone=True),
        Collect("Life insurance matures", money=100),
        Pay("Hospital Fees. Pay $50.", money=50),
        Pay("School fees. Pay $50.", money=50),
        Collect("Receive $25 consultancy fee.", money=25),
        PayForBuildings("You are assessed for street repairs: Pay $40 per house and $115 per hotel you own.",
                        money_per_house=40, money_per_hotel=115),
        Collect("You have won second prize in a beauty contest. Collect $10.", money=10),
        Collect("You inherit $100.", money=100)
    ]
    random.shuffle(cards)
    return cards


def initialize_chance_cards():
    cards = [
        GoTo("Advance to Go. Collect $200.", dest=0),
        GoTo("Advance to Illinois Ave. If you pass Go, collect $200.", dest=24),
        GoTo("Advance to St. Charles Place. If you pass Go, collect $200.", dest=11),
        GoToNearestUtility("Advance token to nearest Utility. If unowned, you may buy it from the Bank. "
                           "If owned, throw dice and pay owner a total 10 (ten) times the amount thrown.",
                           places=[12, 28], mult=10),
        GoToNearestRailroad("Advance token to the nearest Railroad and pay owner twice the rental to which "
                            "he/she is otherwise entitled. If Railroad is unowned, you may buy it from the Bank.",
                            places=[5, 15, 25, 35], mult=2),
        GoToNearestRailroad("Advance token to the nearest Railroad and pay owner twice the rental to which "
                            "he/she is otherwise entitled. If Railroad is unowned, you may buy it from the Bank.",
                            places=[5, 15, 25, 35], mult=2),
        Collect("Bank pays you dividend of $50.", money=50),
        GoTo("Go Back 3 Spaces.", num=-3),
        GoJail("Go to Jail. Go directly to Jail. Do not pass GO, do not collect $200."),
        PayForBuildings("Make general repairs on all your property: For each house pay $25, For each hotel {pay} $100.",
                        money_per_house=25, money_per_hotel=100),
        Pay("Pay poor tax of $15", money=15),
        GoTo("Take a trip to Reading Railroad. If you pass Go, collect $200.", dest=5),
        GoTo("Take a walk on the Boardwalk. Advance token to Boardwalk.", dest=39),
        Pay("You have been elected Chairman of the Board. Pay each player $50", money=50, to_everyone=True),
        Collect("Your building loan matures. Receive $150.", money=150),
        Collect("You have won a crossword competition. Collect $100", money=100)
    ]
    random.shuffle(cards)
    return cards
