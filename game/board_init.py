from classes.card import Card, PropertyCard, RailRoadCard, UtilityCard, TaxCard, Group


def initialize_board():
    go = Card("Go", is_special=True)
    comm_chest = Card("Community Chest", is_community=True)
    luxury_tax = TaxCard("Luxury Tax", tax=100)
    income_tax = TaxCard("Income Tax", tax=200)
    chance = Card("Chance", is_chance=True)
    jail = Card("Jail/Visiting Jail", is_special=True)
    free_parking = Card("Free Parking", is_special=True)
    go_to_jail = Card("Go to Jail", is_go_jail=True)

    reading_rr = RailRoadCard("Reading Railroad")
    penn_rr = RailRoadCard("Pennsylvania Railroad")
    bno_rr = RailRoadCard("B. & O. Railroad")
    short_line_rr = RailRoadCard("Short Line")
    railroads = Group("Railroad", [reading_rr, penn_rr, bno_rr, short_line_rr], 0, is_color=False)

    electric_company = UtilityCard("Electric Company")
    water_works = UtilityCard("Water Works")
    utilities = Group("Utility", [electric_company, water_works], 0, is_color=False)

    med_ave = PropertyCard("Mediterranean Avenue", 60, [2, 10, 30, 90, 160, 250], 30)
    baltic_ave = PropertyCard("Baltic Avenue", 60, [4, 20, 60, 180, 320, 450], 30)
    brown = Group("Brown", [med_ave, baltic_ave], 50)

    oriental_ave = PropertyCard("Oriental Avenue", 100, [6, 30, 90, 270, 400, 550], 50)
    vermont_ave = PropertyCard("Vermont Avenue", 100, [6, 30, 90, 270, 400, 550], 50)
    conn_ave = PropertyCard("Connecticut Avenue", 120, [8, 40, 100, 300, 450, 600], 60)
    light_blue = Group("Light Blue", [oriental_ave, vermont_ave, conn_ave], 50)

    st_charles_place = PropertyCard("St. Charles Place", 140, [10, 50, 150, 450, 625, 750], 70)
    states_ave = PropertyCard("States Avenue", 140, [10, 50, 150, 450, 625, 750], 70)
    virginia_ave = PropertyCard("Virginia Avenue", 160, [12, 60, 180, 500, 700, 900], 80)
    pink = Group("Pink", [st_charles_place, states_ave, virginia_ave], 100)

    st_james_place = PropertyCard("St. James Place", 180, [14, 70, 200, 550, 750, 950], 90)
    ten_ave = PropertyCard("Tennessee Avenue", 180, [14, 70, 200, 550, 750, 950], 90)
    ny_ave = PropertyCard("New York Avenue", 200, [16, 80, 220, 600, 800, 1000], 100)
    orange = Group("Orange", [st_james_place, ten_ave, ny_ave], 100)

    kentucky_ave = PropertyCard("Kentucky Avenue", 220, [18, 90, 250, 700, 875, 1050], 110)
    indiana_ave = PropertyCard("Indiana Avenue", 220, [18, 90, 250, 700, 875, 1050], 110)
    illinois_ave = PropertyCard("Illinois Avenue", 240, [20, 100, 300, 750, 925, 1100], 120)
    red = Group("Red", [kentucky_ave, indiana_ave, illinois_ave], 150)

    atlantic_ave = PropertyCard("Atlantic Avenue", 260, [22, 110, 330, 800, 975, 1150], 130)
    ventnor_ave = PropertyCard("Ventnor Avenue", 260, [22, 110, 330, 800, 975, 1150], 130)
    marvin_gardens = PropertyCard("Marvin Gardens", 280, [24, 120, 360, 850, 1025, 1200], 140)
    yellow = Group("Yellow", [atlantic_ave, ventnor_ave, marvin_gardens], 150)

    pacific_ave = PropertyCard("Pacific Avenue", 300, [26, 130, 390, 900, 1100, 1275], 150)
    nc_ave = PropertyCard("North Carolina Avenue", 300, [26, 130, 390, 900, 1100, 1275], 150)
    penn_ave = PropertyCard("Pennsylvania Avenue", 320, [28, 150, 450, 1000, 1200, 1400], 160)
    green = Group("Green", [pacific_ave, nc_ave, penn_ave], 200)

    park_place = PropertyCard("Park Place", 350, [35, 175, 500, 1100, 1300, 1500], 175)
    boardwalk = PropertyCard("Boardwalk", 400, [50, 200, 600, 1400, 1700, 2000], 200)
    blue = Group("Blue", [park_place, boardwalk], 200)

    board = [go, med_ave, comm_chest, baltic_ave, income_tax, reading_rr, oriental_ave, chance, vermont_ave, conn_ave,
             jail, st_charles_place, electric_company, states_ave, virginia_ave, penn_rr, st_james_place, comm_chest,
             ten_ave, ny_ave, free_parking, kentucky_ave, chance, indiana_ave, illinois_ave, bno_rr, atlantic_ave,
             ventnor_ave, water_works, marvin_gardens, go_to_jail, pacific_ave, nc_ave, comm_chest, penn_ave,
             short_line_rr, chance, park_place, luxury_tax, boardwalk]

    groups = [railroads, utilities, brown, light_blue, pink, orange, red, yellow, green, blue]

    return board, groups
