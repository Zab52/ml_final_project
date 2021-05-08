import sys
import math
import random
import copy


class Othello():
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.board = [[0]*cols] * rows
        self.playerTurn = 0
        self.validMoves = []

    def isMoveValid(self, move):
        row = move[0]
        col = move[1]

        if self.board[row][col] != 0:
            return 0

        



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

    def playMove(self, move):


        self.playerTurn *= -1
