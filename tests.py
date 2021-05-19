from backpropagation import ANN
from othello import Othello
from copy import deepcopy
import pickle
import argparse

"""
A file to run tests given a learner.
Can have the learner play against either a random player, or a heuristic player.
Outputs a score of n games vs. random player.
Outputs a score of 488 games vs. heuristic player.
"""

# Function that plays a game of Othello until it is finished.
def sim_game(game):
    while not game.end:
        game.next_move(None)
    return game.winner

# Simulates num_games games starting from the start of an Othello game.
# Used for testing the learner against the random player.
def random_games(ann,sqaures,num_games,white,black):
    white_wins, black_wins, ties = 0,0,0
    game = Othello(args.squares,args.squares,white,black,ann=ann)
    for i in range(num_games):
        print(i)
        game.new_game()
        winner = sim_game(game)
        if winner == 1:
            white_wins += 1
        elif winner == -1:
            black_wins += 1
        else:
            ties += 1
    return white_wins, black_wins, ties

# Returns a list of Othello games where each game corrsponds to
# a gamestate after moves_remaining moves are played given the initially
# inputted gamestate.
def make_games(current_games,moves_remaining):
    if moves_remaining == 0:
        return current_games
    else:
        next_games = []
        for game in current_games:
            for move in game.find_moves():
                new = deepcopy(game)
                new.play_move(move)
                next_games.append(new)
        return make_games(next_games,moves_remaining-1)

# Simulates games starting from 1 of 244 different possible initial
# gamestates. These gamestates correspond to all the possible
# gamestates after four moves are initially played.
def heur_games(ann,squares,white,black):
    white_wins, black_wins, ties = 0,0,0
    start = Othello(args.squares,args.squares,white,black,ann=ann)
    start.new_game()

    # Creating each of the possible intial board states to be considered.
    games = make_games([start],4)
    i = 0

    # Simulating games starting from each of the initial boards constructed.
    for game in games:
        print('Game', i)
        winner = sim_game(game)
        i += 1
        if winner == 1:
            white_wins += 1
        elif winner == -1:
            black_wins += 1
        else:
            ties += 1
    return white_wins, black_wins, ties


if __name__ == '__main__':
    #parse args
    parser = argparse.ArgumentParser(description='Size of the board and type of Players')
    parser.add_argument("-squares", help="The size of the square Othello board",
                        type=int, default=8)
    parser.add_argument("-games", help="The number of games to learn from",
                        type=int, default=1000)
    parser.add_argument("-opponent", help="The type of opponent",
                        default='random', choices=['random','heur'])
    parser.add_argument("-filename", help="The name of the file to retrieve the ann",
                        default='ann.obj')
    args = parser.parse_args()

    with open(args.filename, 'rb') as filehandler:
        ann = pickle.load(filehandler)

    if args.opponent == 'random':
        learner, rand, ties = random_games(ann,args.squares,args.games//2,'td','random')
        new_rand, new_learner, new_ties = random_games(ann,args.squares,args.games//2,'random','td')
        print('Random Stats:')
        print('Learner:', learner + new_learner)
        print('Random:', rand + new_rand)
        print('Ties:', ties + new_ties)
        print('Percent wins:', ((learner+new_learner) / args.games))
    else:
        learner, heur, ties = heur_games(ann,args.squares,'td','heur')
        new_heur, new_learner, new_ties = heur_games(ann,args.squares,'heur','td')
        print('Heuristic Stats:')
        print('Learner:', learner + new_learner)
        print('Heuristic:', heur + new_heur)
        print('Ties:', ties + new_ties)
        print('Percent wins:', ((learner+new_learner) / 488))
