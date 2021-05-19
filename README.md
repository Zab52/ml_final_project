# Using Temporal Difference Learning to Play Othello

This project contains all the code to train and test a learner using the TD(0) algorithm augmented with a neural network evaluation function. At a high level, there are three main files containing the implementation of the game and the learner, and then three executable script files that allow us to use the learner in different ways:

- Code files
  - `othello.py` contains all of the code representing the game of Othello and the rules
  - `player.py` contains the implementation of the four different types of players: random, heuristic, td-learner, and user. The players take calls from the Othello game and player their next move.
  - `backpropagation.py` contains an implementation of a neural network with one hidden layer. It is copied with very few changes from Week 5.

- Script Files
  - `learner.py` provides a script to create a learner and have it learn to play Othello. It outputs a series of `.obj` files that contain a (non-human readable) version of the learned neural network.
  - `tests.py` allows the user to test the performance of a certain learner against random and heuristic players.
  - `gui.py` runs a TKinter-based GUI and allows the user to either view or play a game of Othello with any two inputted player types

Lastly the folder `ann_results` contains the results of the learning process in the form of stored neural networks. Each of the backups is saved in a file with the associated backup number; multiply that number by 50,000 to see how many games the learner had played up to that point. Backup 0 stores the learner after 10,000 games rather than 0, because we accidentally overwrote our earlier file in trying to make sure that our learner was actually running. The final, 2 million-game learner is stored in `learner.obj`.


## Instructions for Running Scripts
For each of the scripts, run ```python scriptName.py -h``` to see a full list of the arguments (some of which are optional and/or have default values) that it takes.

An example command to launch the GUI is shown below:
```
python GUI.py -black user -white td -filename ann_results/learner.obj
```

The command we used to train our learner is shown below:
```
python learner.py -learningRate 0.01 -exploration_rate 0.1 -games 2000000 -backup 50000 -filename learner.obj
```

An example command to run tests is shown below:
```
python tests.py -opponent heur -filename learner.obj
```

## Important Notes

We based our implementation and training entirely on that described in the following paper:

- Michiel van der Ree and Marco Weiring, "Reinforcement Learning in the Game of Othello: Learning Against a Fixed Opponent and Learning from Self-Play"

However, there are two main notes we want to bring to your attention regarding how our implementation differs from van der Ree and Wiering's. First, we used a learning rate of 0.01, whereas they used a learning rate of 0.001. We thought that sounded extremely low, and we also trained a learner with that learning rate for the 2,000,000 games in parallel with our main learner. It did not perform nearly as well, and did not really appear to learn much at all; for example, it never improved against the heuristic player from the baseline. We do not know for sure what accounts for the discrepancy. Perhaps it is due to the next point, or perhaps something else.

Second, we realized part way through the learning that our implementation differed from theirs in how we applied the temporal difference learning. We backpropagated the error between the estimated value for a state and the calculated value of the state immediately after that; i.e. when it was the opponent's turn. van der Ree and Wiering backpropagated the error between the estimated value for a state and the value of the next state when it was our turn; i.e. a full turn later. We had misunderstood their algorithm and assumed that they had incremented t part way through, but they did not. Both are reasonable attempts to learn; ours probably suffers a bit in that it is estimating the value of a board when it is not our turn. This is probably the main cause for discrepancies between our results and theirs.
