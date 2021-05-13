import sys
import math
import random
import copy
import pickle
from backpropagation import ANN
from player import Player, RandomPlayer, HeurPlayer, UserPlayer, TDPlayer

# Class to store a game of Othello.
class Othello():

    # Initializing the Othello game for any size board.
    def __init__(self, cols, rows, white, black, ann=None,learning=False,
                 explorationRate=0, filename=None):
        self.cols = cols
        self.rows = rows
        self.board = [[0 for i in range(cols)] for j in range(rows)]

        #make users of the type desired
        #black is -1
        #white is 1
        self.black = self.make_user(black,-1,ann,learning,explorationRate, filename)
        self.white = self.make_user(white,1,ann,learning,explorationRate, filename)
        self.playerTurn = 0
        self.end = False
        self.winner = 0

    #create our players based on arguments passed in
    def make_user(self,player,i,ann,learning,explorationRate, filename):
        if player == 'user':
            return UserPlayer(self,i)
        elif player == 'random':
            return RandomPlayer(self,i)
        elif player == 'heur':
            return HeurPlayer(self,i)
        else:
            if filename:
                with open(filename,'rb') as filehandler:
                    ann = pickle.load(filehandler)
            return TDPlayer(self,i,ann=ann,learning=learning,explorationFactor=explorationRate)

    # Function to check if a move is outside the board.
    def outOfBounds(self,row, col):
        if (row < 0 or row >= self.rows or col < 0 or col >= self.cols):
            return 1

        return 0

    # Given a move, this function checks to see if the move is valid for
    # the given game of Othello. Returns 1 if the move is valid. Otherwise,
    # returns 0.
    def isMoveValid(self, move):
        row, col = move

        # Checking to see if the specified move on the board is empty.
        if self.board[col][row] != 0:
            return 0

        directions = [(0,1), (1,0), (1,1), (-1,-1), (-1,0), (0,-1), (1,-1), (-1,1)]

        # Checking around the move specified to check if it is valid.
        for v,h in directions:
            # Checking each of the adjacent tiles of the board.
            checkRow = row + v
            checkCol = col + h

            #check that theres one other piece first
            if ((not self.outOfBounds(checkRow, checkCol)) and
                self.board[checkCol][checkRow] == -1*self.playerTurn):
                checkRow += v
                checkCol += h

                # Continuing in the same direction until a tile is found that
                # is either out of bounds, or not an opponent's piece.
                while ((not self.outOfBounds(checkRow, checkCol)) and
                    self.board[checkCol][checkRow] == -1*self.playerTurn):
                    checkRow += v
                    checkCol += h

                # Checking each of the adjacent tiles of the board.
                # Case where the move must be valid.
                if ((not self.outOfBounds(checkRow, checkCol)) and
                    self.board[checkCol][checkRow] == self.playerTurn):
                    return 1

        # Move isn't valid.
        return 0

    #given a move, update the board accordingly
    def updateBoard(self, row, col):
        self.board[col][row] = self.playerTurn

        directions = [(0,1), (1,0), (1,1), (-1,-1), (-1,0), (0,-1), (1,-1), (-1,1)]

        # Checking around the move specified to check if it is valid.
        for v,h in directions:
            # Checking each of the adjacent tiles of the board.
            checkRow = row + v
            checkCol = col + h

            count = 0

            #check that theres one other piece first
            if ((not self.outOfBounds(checkRow, checkCol)) and
                self.board[checkCol][checkRow] == -1*self.playerTurn):
                checkRow += v
                checkCol += h
                count += 1

                # Continuing in the same direction until a tile is found that
                # is either out of bounds, or not an opponent's piece.
                while ((not self.outOfBounds(checkRow, checkCol)) and
                    self.board[checkCol][checkRow] == -1*self.playerTurn):
                    checkRow += v
                    checkCol += h
                    count += 1

                # Checking each of the adjacent tiles of the board.
                # Case where the move must be valid.
                if ((not self.outOfBounds(checkRow, checkCol)) and
                    self.board[checkCol][checkRow] == self.playerTurn):
                        checkRow -= v
                        checkCol -= h


                        while count > 0:
                            self.board[checkCol][checkRow] = self.playerTurn
                            checkRow -= v
                            checkCol -= h
                            count -= 1


    # Function to start a new game.
    def newGame(self):
        for row in self.board:
            for i in range(self.cols):
                row[i] = 0

        midRow = self.rows//2 -1
        midCol = self.cols//2 -1

        self.board[midRow][midCol] = 1
        self.board[midRow + 1][midCol+1] = 1
        self.board[midRow+1][midCol] = -1
        self.board[midRow][midCol+1] = -1

        self.playerTurn = -1
        self.end = False

    # Function to check if the current player has any valid moves.
    def searchMoves(self):
        for n in range(self.rows):
            for i in range(self.cols):
                if self.isMoveValid((n,i)):
                    return 1

        return 0

    # Called when the game is over. Returns 0 if the game is a draw. Otherwise
    # returns the winner (-1 or 1).
    def gameOver(self):
        score = 0
        self.end = True

        # Evaluating the current board.
        for n in range(self.rows):
            for i in range(self.cols):
                score += self.board[n][i]

        # Determining the winner.
        if score < 0:
            self.winner = -1
        elif score > 0:
            self.winner = 1
        else:
            self.winner = 0

    #find the score at a certain point in the game
    def score(self):
        white, black = 0,0
        for row in self.board:
            for col in row:
                if col == 1:
                    white += 1
                elif col ==-1:
                    black += 1
        return white, black

    # Function to play a given move. If a moved is played, also checks if the
    # game has ended, or if the next player doesn't have any valid moves.
    # Returns 1 if the move was valid, otherwise, returns 0.
    def playMove(self, move):
        self.updateBoard(move[0], move[1])
        self.playerTurn *= -1

        # Checking to see if the players have valid moves.
        if not self.searchMoves():
            self.playerTurn *= -1
            if not self.searchMoves():
                self.gameOver()
        return 1

    #return a list of valid moves
    def find_moves(self):
        moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.isMoveValid((i,j)):
                    moves.append((i,j))
        return moves

    #make the next move
    def next_move(self,user_move):
        if self.end:
            return False
        if self.playerTurn == -1:
            return self.black.make_move(user_move)
        else:
            return self.white.make_move(user_move)

if __name__ == '__main__':
    """
    ann = ANN(16,10,1,0.01)
    for i in range(50000):
        print(i)
        game = Othello(4,4,'td','td',ann)
        game.newGame()
        while not game.end:
            game.next_move(None)
    with open('four_by_four_ann.obj', 'wb') as filehandler:
        pickle.dump(ann, filehandler)
    """
    with open('ann.obj', 'rb') as filehandler:
        ann = pickle.load(filehandler)
    white, black = 0,0
    for i in range(3000):
        print(i)
        game = Othello(4,4,'random','td',ann=ann)
        game.newGame()
        while not game.end:
            game.next_move(None)
        if game.winner == 1:
            white += 1
        elif game.winner == -1:
            black += 1

    print('White:', white)
    print('Black', black)
