Brief Introduction of Othello Player

1. Discription
   The student engine uses both minimax search and alpha-beta pruning.
   And then hash the board state to
    i. check how many duplicated nodes are produced.
    2. restore the heuristic value.

2. Experiment
    i. student vs random1, alpha-beta
        depth = 1, 30 times, win 27, lose 3, average Node 9076, average duplicate 1440.9 for a game.  ave branching factor 4.59
    ii. student vs random1, minimax
        depth = 1, 30 times, win 24, lose 5, tie 1, average Node 16939.6, average duplicate 3676.2 for a game, ave branching factor 7.52
    iii depth and time: alpha-beta
        depth = 1, s, depth = 2, 0.43s/turn, depth = 3, 1.21s/turn
    iv  depth and time: minimax
        depth = 1, 0.60s/move, depth = 2, 1.58s/move,  depth = 3,3.4s/move

    The results shows alpha-beta solves the problem better and explore less nodes.
    


