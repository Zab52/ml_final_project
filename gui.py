#import tkinter as tk

#window = tk.Tk()
# Code to add widgets will go here...

#game = Othello(8,8)
import tkinter
from othello import Othello

size = 80 #the size of a cell in pixels


top = tkinter.Tk()

game = Othello(8,8)
game.newGame()

canvas = tkinter.Canvas(top, bg="green", height=size*game.cols, width=size*game.rows)

for i in range(game.rows + 1):
    line = canvas.create_line(0, i*size, size*game.cols , i*size, fill='black')

for i in range(game.rows + 1):
    line = canvas.create_line(i*size, 0, i*size, size*game.cols, fill='black')


def update_game():
    for i in range(game.cols):
        for j in range(game.rows):
            if game.board[i][j] == 1:
                canvas.create_oval(i*size+1, j*size+1, (i+1)*size-1, (j+1)*size-1,fill='white')
            elif game.board[i][j] == -1:
                canvas.create_oval(i*size+1, j*size+1, (i+1)*size-1, (j+1)*size-1,fill='black')

def make_move(event):
    move = event.y//size, event.x//size
    print('Move', move)
    if game.isMoveValid(move):
        print('made it')
        game.playMove(move)
        update_game()

canvas.bind("<Button-1>", make_move)

update_game()

canvas.pack()
top.mainloop()
