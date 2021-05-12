from backpropagation import ANN
from othello import Othello
import random

class TDZero():
    def __init__(self, inpNum, hiddenNum, learningRate, discountFactor,
        explorationFactor):
        self.evalNetwork = ANN(inpNum, hiddenNum, 1, learningRate)

        self.discountFactor = discountFactor
        self.explorationFactor = explorationFactor

    def create_input_vector(self, board, numCols, turn):
        input = []

        for row in board:
            for i in range(numCols):
                input.append(row[i]*turn)

        return input

    def selectMove(self, nextMoves, game):

        if random.random() < self.explorationFactor:
            bestMove = nextMoves[random.randint(0, len(nextMoves) - 1)]
            board = game.nextBoard(bestMove)
            input = create_input_vector(board, game.cols, game.turn)
            return bestMove,self.evalNetwork.classify(input)[0]


        best = float('-inf')

        for move in nextMoves:
            board = game.nextBoard(move)
            input = self.create_input_vector(board, game.cols, game.playerTurn)
            current = self.evalNetwork.classify(input)[0]

            if best < current:
                best = current
                bestMove = move


        return bestMove,best

    def learn(self, game):
        input = self.create_input_vector(game.board, game.cols, game.playerTurn)

        valid_moves = game.find_moves()

        output = self.evalNetwork.classify(input)[0]

        move,newOutput = self.selectMove(valid_moves, game)

        game.playMove(move)

        if game.end:
            reward = .5

            if game.winner == turn:
                reward = 1
            elif game.winner == -1*turn:
                reward = 0

            newOutput += reward

        self.evalNetwork.backpropagate(input, [newOutput])


testing  = TDZero(64, 50, .001, 1, .1)

game = Othello(8,8, 'user', 'user')

game.newGame()

testing.learn(game)
