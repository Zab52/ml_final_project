import random

class Player():
    def __init__(self,game):
        self.game = game

    def get_move(self):
        moves = self.game.find_moves()
        return random.choice(moves)
