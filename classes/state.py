from classes.game import Game

class State:
    def __init__(self, player, other_players):
        pass
        self.matrix = []
        # Uno cada color, Ferrocarril, Utilidad, Balance dinero/dinero_total
        # color 8:  2: 6/12 12/12
        #           3: 4/12 8/12/ 12/12
        # hip color 8:
        # ferro     4: 1/4 2/4 3/4 4/4
        # utilidade 2: 1/2 2/2
        # balance/2000
        # posicion/40

        #4 columnas 1 para cada jugador
        #20x4

    def get_state(self):
        pass
        #return 20x4 [80]

    def add_property(self, player, prop):
        pass
        # pos[11] - cost
        # color + x/12
        # return [80]