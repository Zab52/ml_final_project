from backpropagation import ANN
from othello import Othello

class TDZero():
    def __init__(self, inpNum, hiddenNum, outNum, learningRate, discountFactor,
        explorationFactor):
        self.evalNetwork = ANN(inpNum, hiddenNum, outNum, learningRate)

        self.discountFactor = discountFactor
        self.explorationFactor = explorationFactor

    def create_input_vector(self, board, numCols, turn):
        input = []

        for row in board:
            for i in range(numcols):
                input.append(row[i]*turn)

        return input

    def selectMove(self, nextMoves, output, numCols):

        if random.random() < self.explorationFactor:
            return nextMoves[random.randint(0, len(nextMoves) - 1)]

        best = float('-inf')

        for move in nextMoves:
            row = move[0]
            col = move[1]

            compare = output[row*numCols + col]
            if compare > best:
                best = compare
                bestMove = move

        return bestMove

    def learn(self, game):
        color = game.turn
        input = self.create_input_vector(game.board, game.cols, color)

        valid_moves = game.find_moves()

        output = self.evalNetwork.classify(input)

        move = self.selectMove(valid_moves, output, game.cols)

        game.playMove(move)

        newInput = self.create_input_vector(game.board, game.cols, color)

        newOutput = self.evalNetwork.classify(newInput)

        if game.end:
            reward = .5

            if game.winner == color:
                reward = 1
            elif game.winner == -1*color:
                reward = 0

            for i in range(len(newOutput)):
                newOutput[i] = reward + self.discountFactor*newOutput[i]

        self.evalNetwork(input, newOutput)
