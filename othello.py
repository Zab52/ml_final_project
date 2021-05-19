import sys
import math
import random
import copy
import pickle
from backpropagation import ANN
from player import Player, RandomPlayer, HeurPlayer, UserPlayer, TDPlayer

"""
Store a game of othello, including board information and player information
Provides methods to find playable moves and update board according to given move
"""

class Othello():

    # Initializing the Othello game for any size board.
    def __init__(self, cols, rows, white, black, ann=None,learning=False,
                 exploration_rate=0):
        self.cols = cols
        self.rows = rows
        self.board = [[0 for i in range(cols)] for j in range(rows)]

        #make users of the type desired
        #black is -1
        #white is 1
        self.black = self.make_user(black,-1,ann,learning,exploration_rate)
        self.white = self.make_user(white,1,ann,learning,exploration_rate)
        self.player_turn = 0
        self.end = False
        self.winner = 0

        # Stores squares on the board that don't have pieces.
        self.open_moves = []

    #create our players based on arguments passed in
    def make_user(self,player,i,ann,learning,exploration_rate):
        if player == 'user':
            return UserPlayer(self,i)
        elif player == 'random':
            return RandomPlayer(self,i)
        elif player == 'heur':
            return HeurPlayer(self,i)
        else:
            return TDPlayer(self,i,ann=ann,learning=learning,explorationFactor=exploration_rate)

    # Function to check if a move is outside the board.
    def out_of_bounds(self,row, col):
        if (row < 0 or row >= self.rows or col < 0 or col >= self.cols):
            return 1

        return 0

    # Given a move, this function checks to see if the move is valid for
    # the given game of Othello. Returns 1 if the move is valid. Otherwise,
    # returns 0.
    def is_move_valid(self, move):
        row, col = move

        # Checking to see if the specified move on the board is empty.
        if self.board[col][row] != 0:
            return 0

        directions = [(0,1), (1,0), (1,1), (-1,-1), (-1,0), (0,-1), (1,-1), (-1,1)]

        # Checking around the move specified to check if it is valid.
        for v,h in directions:
            # Checking each of the adjacent tiles of the board.
            check_row = row + v
            check_col = col + h

            #check that theres one other piece first
            if ((not self.out_of_bounds(check_row, check_col)) and
                self.board[check_col][check_row] == -1*self.player_turn):
                check_row += v
                check_col += h

                # Continuing in the same direction until a tile is found that
                # is either out of bounds, or not an opponent's piece.
                while ((not self.out_of_bounds(check_row, check_col)) and
                    self.board[check_col][check_row] == -1*self.player_turn):
                    check_row += v
                    check_col += h

                # Checking each of the adjacent tiles of the board.
                # Case where the move must be valid.
                if ((not self.out_of_bounds(check_row, check_col)) and
                    self.board[check_col][check_row] == self.player_turn):
                    return 1

        # Move isn't valid.
        return 0

    #given a move, update the board accordingly
    def update_board(self, row, col):
        self.open_moves.remove((row, col))

        #placing the move on the board
        self.update_board_helper(row, col, self.board)

    #given a move, creates a copy of the resulting board without updating
    #the actual board of the game.
    def simulate_next_move(self, move):
        board = copy.deepcopy(self.board)

        row = move[0]
        col = move[1]

        #simulating placing the specified move on the board.
        self.update_board_helper(row, col, board)

        return board

    #given a move and a board, places the move on the board.
    def update_board_helper(self, row, col, board):
        board[col][row] = self.player_turn

        directions = [(0,1), (1,0), (1,1), (-1,-1), (-1,0), (0,-1), (1,-1), (-1,1)]

        # Checking around the move specified to check if it is valid.
        for v,h in directions:
            # Checking each of the adjacent tiles of the board.
            check_row = row + v
            check_col = col + h

            count = 0

            #check that theres one other piece first
            if ((not self.out_of_bounds(check_row, check_col)) and
                board[check_col][check_row] == -1*self.player_turn):
                check_row += v
                check_col += h
                count += 1

                # Continuing in the same direction until a tile is found that
                # is either out of bounds, or not an opponent's piece.
                while ((not self.out_of_bounds(check_row, check_col)) and
                    board[check_col][check_row] == -1*self.player_turn):
                    check_row += v
                    check_col += h
                    count += 1

                # Case where one of the player's pieces are found, implying
                # pieces have been captured.
                if ((not self.out_of_bounds(check_row, check_col)) and
                    board[check_col][check_row] == self.player_turn):
                        check_row -= v
                        check_col -= h

                        # Flipping each piece captured by the move.
                        while count > 0:
                            board[check_col][check_row] = self.player_turn
                            check_row -= v
                            check_col -= h
                            count -= 1



    # Function to start a new game.
    def new_game(self):

        #Initializing the board to being empty.
        for row in self.board:
            for i in range(self.cols):
                row[i] = 0

        # Adding in the starting pieces for the game.
        mid_row = self.rows//2 -1
        mid_col = self.cols//2 -1

        self.board[mid_row][mid_col] = 1
        self.board[mid_row + 1][mid_col+1] = 1
        self.board[mid_row+1][mid_col] = -1
        self.board[mid_row][mid_col+1] = -1

        # Creating the open moves array.
        self.open_moves = []
        for i in range(self.rows):
            for n in range(self.cols):
                if self.board[i][n] == 0:
                    self.open_moves.append((i,n))

        # Setting the player turn.
        self.player_turn = -1
        self.end = False
        self.winner = 0

    # Function to check if the current player has any valid moves.
    def search_moves(self):
        for move in self.open_moves:
            if self.is_move_valid(move):
                return 1

        return 0

    # Called when the game is over. Returns 0 if the game is a draw. Otherwise
    # returns the winner (-1 or 1).
    def game_over(self):
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
    def play_move(self, move):
        self.update_board(move[0], move[1])
        self.player_turn *= -1

        # Checking to see if the players have valid moves.
        if not self.search_moves():
            self.player_turn *= -1
            if not self.search_moves():
                self.game_over()
        return 1

    #return a list of valid moves
    def find_moves(self):
        moves = []
        for move in self.open_moves:
            if self.is_move_valid(move):
                moves.append(move)

        return moves

    #prompt the correct player object to make the next move
    def next_move(self,user_move,values=False):
        if self.end:
            return False
        if self.player_turn == -1:
            return self.black.make_move(user_move,values)
        else:
            return self.white.make_move(user_move,values)
