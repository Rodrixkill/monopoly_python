from classes.card_definitions import Card

MAX_BALANCE = 2000
MAX_POSITION = 40


class State:
    def __init__(self, player, other_players):
        self.player_info = [0] * 23
        self.other_players_info = {p.name: [0] * 23 for p in other_players}
        self.pos = {
            "Brown": 0, "Light Blue": 1, "Pink": 2, "Orange": 3, "Red": 4, "Yellow": 5, "Green": 6, "Blue": 7,
            "Railroad": 8, "Utilities": 9, "Balance": 20, "Pos": 21, "Jail": 22
        }
        # pARA HIPOTECA SUMAS COLOR MAS 10, SERIA DEL 10 AL 19
        self.max_per_color = {
            "Brown": 2, "Light Blue": 3, "Pink": 3, "Orange": 3, "Red": 3, "Yellow": 3, "Green": 3, "Blue": 2,
            "Railroad": 4, "Utilities": 2
        }

        self.player_info[self.pos["Balance"]] = player.balance / MAX_BALANCE
        self.player_info[self.pos["Pos"]] = player.current_pos / MAX_POSITION

        if player.in_jail:
            self.player_info[self.pos["Jail"]] = (3 - player.turns_in_jail) / 3

        for card in player.cards_owned:
            new_value = 1 / self.max_per_color[card.color_group]
            if card.mortgaged:
                pos = 10 + self.pos[card.color_group]
                self.player_info[pos] += new_value
            else:
                pos = self.pos[card.color_group]
                self.player_info[pos] += new_value

        for p in other_players:
            self.other_players_info[p.name][self.pos["Balance"]] = p.balance / MAX_BALANCE
            self.other_players_info[p.name][self.pos["Pos"]] = p.current_pos / MAX_POSITION
            if p.in_jail:
                self.other_players_info[p.name][self.pos["Jail"]] = (3 - player.turns_in_jail) / 3
            for card in p.cards_owned:
                new_value = 1 / self.max_per_color[card.color_group]
                if card.mortgaged:
                    pos = 10 + self.pos[card.color_group]
                    self.other_players_info[p.name][pos] += new_value
                else:
                    pos = self.pos[card.color_group]
                    self.other_players_info[p.name][pos] += new_value

        # Uno cada color incluye ferrocarril y utilidad, Balance dinero/dinero_total
        # color 10:  2: 6/12 12/12
        #           3: 4/12 8/12/ 12/12
        # hip color 10:
        # balance/MAX_BALANCE
        # posicion/40

        # 4 columnas 1 para cada jugador
        # 23x4

    def get_state(self):
        flattened = self.player_info
        for key in self.other_players_info:
            flattened += self.other_players_info[key]
        return flattened

    def add_property(self, prop: Card):
        color_pos = self.pos[prop.color_group]
        new_value = 1 / self.max_per_color[prop.color_group]

        self.player_info[color_pos] += new_value
        self.player_info[self.pos['Balance']] -= prop.card_cost / MAX_BALANCE
        return self.get_state()

    def mortgage_property(self, prop):
        color_pos = self.pos[prop.color_group]
        new_value = 1 / self.max_per_color[prop.color_group]
        self.player_info[color_pos] -= new_value
        self.player_info[color_pos + 10] += new_value
        self.player_info[self.pos['Balance']] += (prop.card_cost / 2) / MAX_BALANCE
        return self.get_state()

    def buy_mortgage_property(self, prop):
        color_pos = self.pos[prop.color_group]
        new_value = 1 / self.max_per_color[prop.color_group]
        self.player_info[color_pos] += new_value
        self.player_info[color_pos + 10] -= new_value
        self.player_info[self.pos['Balance']] -= ((prop.card_cost / 2) * 1.1) / MAX_BALANCE
        return self.get_state()

    def pay_rent(self, prop):
        color_pos = self.pos[prop.color_group]
        owner_name = prop.owner.name
        if not prop.mortgaged:
            if prop.houses_built == 0 and self.other_players_info[owner_name][color_pos] == 1:
                rent = 2 * prop.rent_prices[0]
            elif prop.houses_built > 0:
                rent = prop.rent_prices[prop.houses_built]
            else:
                rent = prop.rent_prices[0]
            self.player_info[self.pos['Balance']] -= rent / MAX_BALANCE
        return self.get_state()

    def leave_jail_paying(self):
        self.player_info[self.pos['Balance']] -= 50 / MAX_BALANCE
        self.player_info[self.pos["Jail"]] = 0
        return self.get_state()

    def leave_jail_rolling(self):
        self.player_info[self.pos["Jail"]] -= 1 / 3
        return self.get_state()

    def end_turn(self):
        return self.get_state()
