from backpropagation import ANN
from othello import Othello
from time import time
import pickle
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Size of the board and type of Players')
    parser.add_argument("-squares", help="The size of the square Othello board",
                        type=int, default=8)
    parser.add_argument("-hidden", help="The number of hidden nodes",
                        type=int, default=50)
    parser.add_argument("-learningRate", help="The learning rate of the neural net",
                        type=float, default=0.01)
    parser.add_argument("-explorationRate", help="The exploration rate of our learner",
                        type=float, default=0.1)
    parser.add_argument("-games", help="The number of games to learn from",
                        type=int, default=1000)
    parser.add_argument("-filename", help="The name of the file to pickle the ann",default='ann.obj')
    args = parser.parse_args()


    ann = ANN(args.squares**2,args.hidden,1,args.learningRate)

    explo = args.explorationRate

    for i in range(args.games):
        newExplo = explo * (1-(i/args.games))
        print('Game', i)
        game = Othello(args.squares,args.squares,'td','td',ann=ann,learning=True,
                        explorationRate=newExplo)
        game.newGame()
        while not game.end:
            game.next_move(None)

    with open(args.filename, 'wb') as filehandler:
        pickle.dump(ann, filehandler)
