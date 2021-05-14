import random
from copy import deepcopy
from backpropagation import ANN

class Player():
    def __init__(self,game,i):
        self.game = game
        self.i = i

    def make_move(self,_):
        pass

class RandomPlayer(Player):
    def __init__(self,game,i):
        Player.__init__(self,game,i)

    def make_move(self,_):
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

    def make_move(self,_):
        moves = self.game.find_moves()
        best = None
        best_score = float('-inf')
        for move in moves:
            after_game = self.game.simulate_next_move(move)
            score = 0
            for i in range(game.rows):
                for j in range(game.cols):
                    score += after_game[i][j] * self.weights[i][j]
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
    def __init__(self,game,i,ann=None,explorationFactor=0.1,learning=False):
        Player.__init__(self,game,i)
        self.ann = ann
        if not self.ann:
            self.ann = ANN(64,50,1,0.01)
        self.explorationFactor = explorationFactor
        self.learning = learning

    def create_input_vector(self,board):
        input = []

        for row in board:
            for entry in row:
                input.append(self.i*entry)

        return input

    def make_move(self,_):
        if self.learning:
            return self.make_move_and_learn()
        else:
            move, _ = self.get_best_move()
            self.game.playMove(move)
            return True

    def get_best_move(self):
        moves = self.game.find_moves()
        best = float('-inf')
        for move in moves:
            after_game = self.game.simulate_next_move(move)
            input = self.create_input_vector(after_game)
            current = self.ann.classify(input)[0]
            if current > best:
                best = current
                bestMove = move
        return bestMove,best

    def make_move_and_learn(self):
        #get new move
        input = self.create_input_vector(self.game.board)
        if random.random() < self.explorationFactor:
            moves = self.game.find_moves()
            self.game.playMove(random.choice(moves))
            next = self.create_input_vector(self.game.board)
            newOutput = self.ann.classify(next)[0]
        else:
            move, newOutput = self.get_best_move()
            self.game.playMove(move)

        #backprop
        if self.game.end:
            reward = .5

            if self.game.winner == self.i:
                reward = 1
            elif self.game.winner == -1*self.i:
                reward = 0

            newOutput += reward

        self.ann.backpropagate(input, [newOutput])
        return True
