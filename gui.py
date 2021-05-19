import tkinter as tk
import argparse
import pickle
from othello import Othello
from backpropagation import ANN

"""
The code for the graphical user interface
Displays games in the usual Othello style
Can simulate games with and against any type of player
"""

size = 80 #the size of a cell in pixels

class GUI():

    #make the GUI, initialize everything to start the game
    def __init__(self, squares, white, black,ann,values):
        self.squares, self.white, self.black, self.ann, self.values = squares, white, black, ann, values
        self.root = tk.Tk()
        self.btn = tk.Button(self.root, text = 'New Game', bd = '5')
        self.btn.bind("<Button-1>", self.new_game)
        self.game = Othello(squares,squares,white,black,ann=ann)
        self.game.new_game()
        self.size = 80
        self.canvas = tk.Canvas(self.root, bg="green", height=self.size*self.game.cols,
                                     width=self.size*self.game.rows)
        self.make_canvas()
        self.update_game()
        self.canvas.bind("<Button-1>", self.make_move)
        self.scoreboard = tk.Label(self.root)
        self.show_score()
        self.turn_label = tk.Label()
        self.update_turn()
        self.btn.pack()
        self.canvas.pack()
        self.scoreboard.pack()
        self.turn_label.pack()
        self.root.mainloop()

    #start a new game from scratch if requested
    def new_game(self,event):
        self.root.destroy()
        self.__init__(self.squares,self.white,self.black, self.ann,self.values)

    #make the othello board
    def make_canvas(self):
        for i in range(self.game.rows + 1):
            line = self.canvas.create_line(0, i*self.size, self.size*self.game.cols , i*self.size, fill='black')

        for i in range(self.game.rows + 1):
            line = self.canvas.create_line(i*self.size, 0, i*self.size, self.size*self.game.cols, fill='black')

    #show the current score of the game
    def show_score(self):
        white, black = self.game.score()
        self.scoreboard.configure(text=f'White: {white}, Black: {black}')

    #after a turn, update whose turn it is (or if game is over)
    def update_turn(self):
        if self.game.end:
            if self.game.winner == 0:
                self.turn_label.configure(text='Game Over. It\'s a tie!')
            else:
                winner = 'White' if self.game.winner == 1 else 'Black'
                self.turn_label.configure(text=f'Game Over. {winner} won!')
        else:
            player = 'White' if self.game.player_turn == 1 else 'Black'
            self.turn_label.configure(text=f'It is now {player}\'s turn.')

    #after a turn, place a flip pieces accordingly
    #actually, this only overwrites on top, but that is fine, as no piece is moved
    def update_game(self):
        for i in range(self.game.cols):
            for j in range(self.game.rows):
                if self.game.board[i][j] == 1:
                    self.canvas.create_oval(i*self.size+1, j*self.size+1, (i+1)*self.size-1, (j+1)*self.size-1,fill='white')
                elif self.game.board[i][j] == -1:
                    self.canvas.create_oval(i*self.size+1, j*self.size+1, (i+1)*self.size-1, (j+1)*self.size-1,fill='black')

    #handle the user making a move by finding where they clicked
    #if any other type of user, just make their move on click
    def make_move(self,event):
        move = event.y//size, event.x//size
        success = self.game.next_move(move,values=self.values)
        if success:
            if self.values:
                print('Next Turn:')
            self.update_game()
            self.show_score()
            self.update_turn()

#parse arguments and create GUI
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Size of the board and type of Players')
    parser.add_argument("-squares", help="The size of the square Othello board",
                        type=int, default=8)
    parser.add_argument("-black", help="The type of the black player",
                        default='user', choices=['user', 'random', 'heur', 'td'])
    parser.add_argument("-white", help="The type of the white player",
                        default='random', choices=['user', 'random', 'heur', 'td'])
    parser.add_argument("-filename", help="The filename storing the pickled ann",default=None)
    parser.add_argument("--values", action='store_true',
                        help="Prints td/heur estimated values to stdout for each move")
    args = parser.parse_args()

    #if supplied a neural net, use it
    ann = None
    if args.filename:
        with open(args.filename, 'rb') as filehandler:
            ann = pickle.load(filehandler)

    app = GUI(args.squares,args.white,args.black,ann,args.values)
