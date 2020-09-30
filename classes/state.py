from classes.card_definitions import Card

MAX_BALANCE = 2000
MAX_POSITION = 40


class State:
    def __init__(self, player, other_players):
        self.player_info = [0] * 10
        self.other_players_info = [0] * 10
        self.pos = {
            "Brown": 0, "Light Blue": 1, "Pink": 2, "Orange": 3, "Red": 4, "Yellow": 5, "Green": 6, "Blue": 7,
            "Railroad": 8, "Utilities": 9
        }
        # pARA HIPOTECA SUMAS COLOR MAS 10, SERIA DEL 10 AL 19
        self.max_per_color = {
            "Brown": 2, "Light Blue": 3, "Pink": 3, "Orange": 3, "Red": 3, "Yellow": 3, "Green": 3, "Blue": 2,
            "Railroad": 4, "Utilities": 2
        }

        for card in player.cards_owned:
            new_value = self.max_per_color[card.color_group] / 17
            new_value += card.houses_built / 17
            pos = self.pos[card.color_group]
            self.player_info[pos] += new_value

        for p in other_players:
            for card in p.cards_owned:
                new_value = self.max_per_color[card.color_group] / 17
                new_value += card.houses_built / 17
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

