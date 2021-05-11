import tkinter as tk
from othello import Othello

size = 80 #the size of a cell in pixels

class GUI():

    def __init__(self):
        self.root = tk.Tk()
        self.btn = tk.Button(self.root, text = 'New Game', bd = '5')
        self.btn.bind("<Button-1>", self.new_game)
        self.game = Othello(8,8)
        self.game.newGame()
        self.size = 80
        self.canvas = tk.Canvas(self.root, bg="green", height=self.size*self.game.cols,
                                     width=self.size*self.game.rows)
        self.make_canvas()
        self.update_game()
        self.canvas.bind("<Button-1>", self.make_move)
        self.scoreboard = tk.Label(self.root)
        self.show_score()
        self.last_move = None
        self.turn_label = tk.Label()
        self.update_turn()
        self.btn.pack()
        self.canvas.pack()
        self.scoreboard.pack()
        self.turn_label.pack()
        self.root.mainloop()


    def new_game(self,event):
        self.root.destroy()
        self.__init__()

    def make_canvas(self):
        for i in range(self.game.rows + 1):
            line = self.canvas.create_line(0, i*self.size, self.size*self.game.cols , i*self.size, fill='black')

        for i in range(self.game.rows + 1):
            line = self.canvas.create_line(i*self.size, 0, i*self.size, self.size*self.game.cols, fill='black')

    def show_score(self):
        white, black = self.game.score()
        self.scoreboard.configure(text=f'White: {white}, Black: {black}')

    def update_turn(self):
        if self.game.end:
            if self.game.winner == 0:
                self.turn_label.configure(text='Game Over. It\'s a tie!')
            else:
                winner = 'White' if self.game.winner == 1 else 'Black'
                self.turn_label.configure(text=f'Game Over. {winner} won!')
        else:
            player = 'White' if self.game.playerTurn == 1 else 'Black'
            self.turn_label.configure(text=f'Last Move: {self.last_move}. It is now {player}\'s turn.')


    def update_game(self):
        for i in range(self.game.cols):
            for j in range(self.game.rows):
                if self.game.board[i][j] == 1:
                    self.canvas.create_oval(i*self.size+1, j*self.size+1, (i+1)*self.size-1, (j+1)*self.size-1,fill='white')
                elif self.game.board[i][j] == -1:
                    self.canvas.create_oval(i*self.size+1, j*self.size+1, (i+1)*self.size-1, (j+1)*self.size-1,fill='black')


    def make_move(self,event):
        if self.game.playerTurn == -1:
            move = event.y//size, event.x//size
        else:
            move = self.game.white.get_move()
        print(move)
        if self.game.isMoveValid(move):
            self.last_move = move
            self.game.playMove(move)
            self.update_game()
            self.show_score()
            self.update_turn()


app = GUI()
