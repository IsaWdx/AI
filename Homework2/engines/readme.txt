Brief Introduction of Othello Player

1. Discription
   The student engine uses both minimax search and alpha-beta pruning.
   And then hash the board state to
    i. check how many duplicated nodes are produced.
    2. restore the heuristic value.

2. Experiment
    i. student vs random1, alpha-beta
        depth = 1, 30 times, win 25, lose 5, average Node 9076, average duplicate 1440.9 ave branching factor 4.59
    ii. student vs random1, minimax
        depth = 1, 30 times, win 18, lose 11, tie 1, average Node 16939.6, average duplicate 3676.2, ave branching factor 7.52
    iii depth and time: alpha-beta
        depth = 1, 23.2s, depth = 2, 32.5s, depth = 3, 48s
    iv  depth and time: minimax
        depth = 1, 4.4s, depth = 2, 8.4s,  depth = 3, 156.2s

    The results shows alpha-beta solves the problem better and explore less nodes.
    Alpha-beta methods has some overhead so it is slower when the depth is low, but
    grows slowly as depth grows.

