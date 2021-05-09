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

    def outOfBounds(row, col):
        if (row < 0 or row >= self.rows or col < 0 or col >- self.cols):
            return 1

        return 0

    def isMoveValid(self, move):
        row = move[0]
        col = move[1]

        if self.board[row][col] != 0:
            return 0

        directions = [(0,1), (1,0), (1,1), (-1,-1), (-1,0), (0,-1), (1,-1), (-1,1)]

        for dir in directions:
            checkRow = row + dir[0]
            checkCol = col + dir[1]

            if self.outOfBounds(checkRow, checkCol):
                continue

            if self.board[checkRow][checkCol] == -1*self.playerTurn:
                checkRow += dir[0]
                checkCol += dir[1]

                while ((not self.outOfBounds(checkRow, checkCol)) and
                    self.board[checkRow][checkCol] == -1*self.playerTurn):
                    checkRow += dir[0]
                    checkCol += dir[1]

                if (not self.outOfBounds(checkRow, checkCol)):
                    return 1

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
        if self.isMoveValid(move):
            self.board[move[0]][move[1]] = self.playerTurn

        self.playerTurn *= -1
