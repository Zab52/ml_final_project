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
        self.board = [[0]*cols] * rows
        self.playerTurn = 0
        self.validMoves = []

    # Function to check if a move is outside the board.
    def outOfBounds(row, col):
        if (row < 0 or row >= self.rows or col < 0 or col >- self.cols):
            return 1

        return 0

    # Given a move, this function checks to see if the move is valid for
    # the given game of Othello. Returns 1 if the move is valid. Otherwise,
    # returns 0.
    def isMoveValid(self, move):
        row = move[0]
        col = move[1]

        # Checking to see if the specified move on the board is empty.
        if self.board[row][col] != 0:
            return 0

        directions = [(0,1), (1,0), (1,1), (-1,-1), (-1,0), (0,-1), (1,-1), (-1,1)]

        # Checking around the move specified to check if it is valid.
        for dir in directions:

            # Checking each of the adjacent tiles of the board.
            checkRow = row + dir[0]
            checkCol = col + dir[1]

            # Case where the tile checked is outside of the board.
            if self.outOfBounds(checkRow, checkCol):
                continue

            # Case where an adjacent tile an opponent's piece.
            if self.board[checkRow][checkCol] == -1*self.playerTurn:
                checkRow += dir[0]
                checkCol += dir[1]

                # Continuing in the same direction until a tile is found that
                # is either out of bounds, or not an opponent's piece.
                while ((not self.outOfBounds(checkRow, checkCol)) and
                    self.board[checkRow][checkCol] == -1*self.playerTurn):
                    checkRow += dir[0]
                    checkCol += dir[1]

                # Case where the move must be valid.
                if (not self.outOfBounds(checkRow, checkCol)):
                    return 1

        # Move isn't valid.
        return 0


    # Function to start a new game.
    def newGame(self):
        for row in self.board:
            for i in range(self.cols):
                row[i] = 0

        midRow = self.rows/2 -1
        midCol = self.col/2 -1

        self.board[midRow][midCol] = 1
        self.board[midRow + 1][midCol+1] = 1
        self.board[midRow+1][midCol] = -1
        self.board[midRow][midCol+1] = -1

        self.playerTurn = 1

    # Function to play a given move.
    def playMove(self, move):
        if self.isMoveValid(move):
            self.board[move[0]][move[1]] = self.playerTurn

        self.playerTurn *= -1
