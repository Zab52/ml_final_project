import sys
import math
import random
import copy

# Class to store a game of Othello.
class Othello():

    # Initializing the Othello game for any size board.
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.board = [[0 for i in range(cols)] for j in range(rows)]
        self.playerTurn = 1
        self.end = False
        self.winner = 0

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
        if self.board[row][col] != 0:
            return 0

        directions = [(0,1), (1,0), (1,1), (-1,-1), (-1,0), (0,-1), (1,-1), (-1,1)]

        # Checking around the move specified to check if it is valid.
        for v,h in directions:
            # Checking each of the adjacent tiles of the board.
            checkRow = row + h
            checkCol = col + v

            #check that theres one other piece first
            if ((not self.outOfBounds(checkRow, checkCol)) and
                self.board[checkRow][checkCol] == -1*self.playerTurn):
                checkRow += v
                checkCol += h

                # Continuing in the same direction until a tile is found that
                # is either out of bounds, or not an opponent's piece.
                while ((not self.outOfBounds(checkRow, checkCol)) and
                    self.board[checkRow][checkCol] == -1*self.playerTurn):
                    checkRow += v
                    checkCol += h

                print(checkRow,checkCol)
                # Checking each of the adjacent tiles of the board.
                # Case where the move must be valid.
                if ((not self.outOfBounds(checkRow, checkCol)) and
                    self.board[checkRow][checkCol] == self.playerTurn):
                    return 1

        # Move isn't valid.
        return 0


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

        self.playerTurn = 1
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
        self.winner = 0

    # Function to play a given move. If a moved is played, also checks if the
    # game has ended, or if the next player doesn't have any valid moves.
    # Returns 1 if the move was valid, otherwise, returns 0.
    def playMove(self, move):
        if self.isMoveValid(move):
            self.board[move[0]][move[1]] = self.playerTurn
            self.playerTurn *= -1

            # Checking to see if the players have valid moves.
            if not self.searchMoves():
                self.playerTurn *= -1
                if not self.searchMoves():
                    self.gameOver()

            return 1
        else:
            return 0
