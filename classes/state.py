from classes.game import Game
from classes.card_definitions import Card

MAX_BALANCE = 2000


class State:
    def __init__(self, player, other_players):
        self.player_info = [0] * 48
        self.other_players_info = {p.name: [0] * 48 for p in other_players}
        self.pos = {
            "Brown": 0, "Light Blue": 1, "Pink": 2, "Orange": 3, "Red": 4, "Yellow": 5, "Green": 6, "Blue": 7,
            "Railroad": 8, "Utilities": 9, "Balance": 20, "Pos": 21
        }
        # pARA HIPOTECA SUMAS COLOR MAS 10, SERIA DEL 10 AL 19
        self.max_per_color = {
            "Brown": 2, "Light Blue": 3, "Pink": 3, "Orange": 3, "Red": 3, "Yellow": 3, "Green": 3, "Blue": 2,
            "Railroad": 4, "Utilities": 2
        }
        for card in player.cards_owned:
            if card.mortgaged:
                pos = 10 + self.pos[card.color_group]
                if self.max_per_color[card.color_group] == 2:
                    self.player_info[pos] += 6 / 12
                elif self.max_per_color[card.color_group] == 3:
                    self.player_info[pos] += 4 / 12
                elif self.max_per_color[card.color_group] == 4:
                    self.player_info[pos] += 3 / 12
            else:
                pos = self.pos[card.color_group]
                if self.max_per_color[card.color_group] == 2:
                    self.player_info[pos] += 6 / 12
                elif self.max_per_color[card.color_group] == 3:
                    self.player_info[pos] += 4 / 12
                elif self.max_per_color[card.color_group] == 4:
                    self.player_info[pos] += 3 / 12
        for p in other_players:
            for card in p.cards_owned:
                if card.mortgaged:
                    pos = 10 + self.pos[card.color_group]
                    if self.max_per_color[card.color_group] == 2:
                        self.other_players_info[p.name][pos] += 6 / 12
                    elif self.max_per_color[card.color_group] == 3:
                        self.other_players_info[p.name][pos] += 4 / 12
                    elif self.max_per_color[card.color_group] == 4:
                        self.other_players_info[p.name][pos] += 3 / 12
                else:
                    pos = self.pos[card.color_group]
                    if self.max_per_color[card.color_group] == 2:
                        self.other_players_info[p.name][pos] += 6 / 12
                    elif self.max_per_color[card.color_group] == 3:
                        self.other_players_info[p.name][pos] += 4 / 12
                    elif self.max_per_color[card.color_group] == 4:
                        self.other_players_info[p.name][pos] += 3 / 12

        # Uno cada color incluye ferrocarril y utilidad, Balance dinero/dinero_total
        # color 10:  2: 6/12 12/12
        #           3: 4/12 8/12/ 12/12
        # hip color 10:
        # balance/MAX_BALANCE
        # posicion/40

        # 4 columnas 1 para cada jugador
        # 22x4

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
