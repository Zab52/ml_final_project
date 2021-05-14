import random
from copy import deepcopy
from backpropagation import ANN

"""
Contains each different type of player, and the functionality for them to
pick their next move and (in the case of the td player) learn
"""

#a super class that defines the basic operations of each player
class Player():
    def __init__(self,game,i):
        self.game = game
        self.i = i

    def make_move(self,_):
        pass

#random player class
class RandomPlayer(Player):
    def __init__(self,game,i):
        Player.__init__(self,game,i)

    #find valid moves and pick one randomly
    def make_move(self,_):
        moves = self.game.find_moves()
        self.game.play_move(random.choice(moves))
        return True

#the heuristic player described in van der Ree and Wiering
class HeurPlayer(Player):
    def __init__(self,game,i):
        Player.__init__(self,game,i)
        #initialize evaluation matrix
        self.weights = [[100,-25,10,5,5,10,-25,100],
                        [-25,-25,2,2,2,2,-25,-25],
                        [10,2,5,1,1,5,2,10],
                        [5,2,1,2,2,1,2,5],
                        [5,2,1,2,2,1,2,5],
                        [10,2,5,1,1,5,2,10],
                        [-25,-25,2,2,2,2,-25,-25],
                        [100,-25,10,5,5,10,-25,100]]

    #pick a move by finding valid moves, evaluating the value of each using
    #the linear function from van der Ree and Wiering, and pick the best
    def make_move(self,_):
        moves = self.game.find_moves()
        best = None
        best_score = float('-inf')
        for move in moves:
            after_game = self.game.simulate_next_move(move)
            score = 0
            #evaluation function

            for i in range(self.game.rows):
                for j in range(self.game.cols):
                    score += after_game[i][j] * self.weights[i][j]
            score *= self.i

            #find best
            if score > best_score:
                best_score = score
                best = move
        self.game.play_move(best)
        return True

#Allows the user to make a move
class UserPlayer(Player):
    def __init__(self,game,i):
        Player.__init__(self,game,i)

    #if move was valid (if user clicked on a 'good') square, make move
    #else do nothing
    def make_move(self,m):
        if self.game.is_move_valid(m):
            self.game.play_move(m)
            return True
        return False

#Our learning player
class TDPlayer(Player):
    def __init__(self,game,i,ann=None,explorationFactor=0.1,learning=False):
        Player.__init__(self,game,i)
        self.ann = ann
        if not self.ann:
            #initialize to a reasonable ANN if none given
            #more for testing rather than anything else
            self.ann = ANN(game.cols*game.rows,50,1,0.01)
        self.explorationFactor = explorationFactor
        self.learning = learning

    #create the input vector to the neural net based on the board
    def create_input_vector(self,board):
        input = []

        for row in board:
            for entry in row:
                #account for whose turn it is
                input.append(self.i*entry)

        return input

    #make the next move, and either learn from it or not
    def make_move(self,_):
        if self.learning:
            return self.make_move_and_learn()
        else:
            move, _ = self.get_best_move()
            self.game.play_move(move)
            return True

    #find the best move from the neural net
    #return move and value of the afterstate
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

    #make a move and perform learning via the neural net
    def make_move_and_learn(self):
        #get new move
        input = self.create_input_vector(self.game.board)
        if random.random() < self.explorationFactor:
            #if we want to explore, just pick a random move and find value
            moves = self.game.find_moves()
            self.game.play_move(random.choice(moves))
            next = self.create_input_vector(self.game.board)
            newOutput = self.ann.classify(next)[0]
        else:
            #pick best move and get value
            move, newOutput = self.get_best_move()
            self.game.play_move(move)

        #backpropagate the error in the value of the previous state
        if self.game.end:
            reward = .5

            if self.game.winner == self.i:
                reward = 1
            elif self.game.winner == -1*self.i:
                reward = 0

            newOutput += reward

        self.ann.backpropagate(input, [newOutput])
        return True
