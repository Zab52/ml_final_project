from backpropagation import ANN
from othello import Othello
import pickle
import argparse

"""
Script to train the learner on a given number of games
Will also backup the ANN to a file a given number of times
"""

if __name__ == '__main__':
    #parse args
    parser = argparse.ArgumentParser(description='Size of the board and type of Players')
    parser.add_argument("-squares", help="The size of the square Othello board",
                        type=int, default=8)
    parser.add_argument("-hidden", help="The number of hidden nodes",
                        type=int, default=50)
    parser.add_argument("-learningRate", help="The learning rate of the neural net",
                        type=float, default=0.01)
    parser.add_argument("-exploration_rate", help="The exploration rate of our learner",
                        type=float, default=0.1)
    parser.add_argument("-games", help="The number of games to learn from",
                        type=int, default=1000)
    parser.add_argument("-backup", help="How often we want to backup (in games)",
                        type=int, default=10000)
    parser.add_argument("-filename", help="The name of the file to pickle the ann",default='ann.obj')
    args = parser.parse_args()


    #learn
    ann = ANN(args.squares**2,args.hidden,1,args.learningRate)
    for i in range(args.games):
        if i%args.backup == 0 or i == 10000:
            #backup the ANN at its current state
            with open('backup_' + str(i//args.backup) + args.filename, 'wb') as filehandler:
                pickle.dump(ann, filehandler)
        newExplo = args.exploration_rate * (1-(i/args.games)) #linearly decrease exploration
        print('Game', i) #for sanity

        #play game
        game = Othello(args.squares,args.squares,'td','td',ann=ann,learning=True,
                        exploration_rate=newExplo)
        game.new_game()
        while not game.end:
            game.next_move(None)

    #save final network
    with open(args.filename, 'wb') as filehandler:
        pickle.dump(ann, filehandler)
