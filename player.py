import random
from copy import deepcopy

class Player():
    def __init__(self,game,i):
        self.game = game
        self.i = i

    def make_move(self,m):
        pass

class RandomPlayer(Player):
    def __init__(self,game,i):
        Player.__init__(self,game,i)

    def make_move(self,m):
        moves = self.game.find_moves()
        self.game.playMove(random.choice(moves))
        return True

class HeurPlayer(Player):
    def __init__(self,game,i):
        Player.__init__(self,game,i)
        self.weights = [[100,-25,10,5,5,10,-25,100],
                        [-25,-25,2,2,2,2,-25,-25],
                        [10,2,5,1,1,5,2,10],
                        [5,2,1,2,2,1,2,5],
                        [5,2,1,2,2,1,2,5],
                        [10,2,5,1,1,5,2,10],
                        [-25,-25,2,2,2,2,-25,-25],
                        [100,-25,10,5,5,10,-25,100]]

    def make_move(self,m):
        moves = self.game.find_moves()
        best = None
        best_score = float('-inf')
        for move in moves:
            after_game = deepcopy(self.game)
            after_game.playMove(move)
            score = 0
            for i in range(after_game.rows):
                for j in range(after_game.cols):
                    score += after_game.board[i][j] * self.weights[i][j]
            score *= self.i
            if score > best_score:
                best_score = score
                best = move
        self.game.playMove(best)
        return True

class UserPlayer(Player):
    def __init__(self,game,i):
        Player.__init__(self,game,i)

    def make_move(self,m):
        if self.game.isMoveValid(m):
            self.game.playMove(m)
            return True
        return False


class TDPlayer(Player):
    def __init__(self,game,i):
        Player.__init__(self,game,i)

    def make_move(self,m):
        moves = self.game.find_moves()
        self.game.playMove(random.choice(moves))
        return True
