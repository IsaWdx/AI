from engines import Engine
from copy import deepcopy


class StudentEngine(Engine):
    """ Game engine that you should you as skeleton code for your 
    implementation. """

    alpha_beta = False
    my_color = 0  # 1 = white, -1 = black

    STATIC_MAX_DEPTH = 2
    DYNAMIC_MAX_DEPTH = 3
    MAX_VALUE = 99999
    BOARD_VALUE = [
        [120, -20, 20, 5, 5, 20, -20, 120],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [20, -5, 15, 3, 3, 15, -5, 20],
        [5, -5, 3, 3, 3, 3, -5, 5],
        [5, -5, 3, 3, 3, 3, -5, 5],
        [20, -5, 15, 3, 3, 15, -5, 20],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [120, -20, 20, 5, 5, 20, -20, 120]
    ]

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Wrapper function that chooses either vanilla minimax or 
        alpha-beta. """
        # print type(board)
        f = self.get_ab_minimax_move if self.alpha_beta else self.get_minimax_move
        return f(board, color, move_num, time_remaining, time_opponent)

    def get_minimax_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):

        # Get a list of all legal moves.
        self.my_color = color
        moves = board.get_legal_moves(color)

        # if time_remaining > 15.0:
        #     count = board.count(color) + board.count(color * -1)
        #     if count % 2 == 1:
        #         count -= 1
        #     if count % 8 == 0:
        #         self.STATIC_MAX_DEPTH = self.DYNAMIC_MAX_DEPTH
        
        # Return the best move according to max-min decision
        return max(moves, key=lambda move: self._get_minimax_value(board, color, move, 1))

    def get_ab_minimax_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Skeleton code from greedy.py to get you started. """
        # Get a list of all legal moves.
        moves = board.get_legal_moves(color)
        
        # Return the best move according to our simple utility function:
        # which move yields the largest different in number of pieces for the
        # given color vs. the opponent?
        return max(moves, key=lambda move: self._get_minimax_alphabeta_value(board, color,
                                                                             move, -self.MAX_VALUE, self.MAX_VALUE, 0))

    def _get_heuristics_value(self, board, game_over = False):
        """ Calculate heuristics value for my color in board
            H(Board) =
                sigma(square_value) | all square in my color
              - sigma(square_value) | all square in opponent's color
              + expected_move_value_for_my_color
        """

        my_color = self.my_color
        op_color = my_color * -1

        # if win, give a big value, don't care the board
        if game_over:
            my_count = board.count(my_color)
            op_count = board.count(op_color)
            if my_count > op_count:
                return 10000
            else:
                return -10000
        my_count = board.count(my_color)
        op_count = board.count(op_color)

        # parity
        if my_count > op_count:
            p = 100 * my_count / (my_count + op_count)
        elif my_count < op_count:
            p = -100 * op_count / (my_count + op_count)
        else:
            p = 0

        # corner:
        scale = 25
        c = 0
        # print board[0][0]
        # print board[1][2]
        for corner in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if board[corner[0]][corner[1]] == 0:
                    if 0 <= corner[0] + move[0] <= 7 and 0 <= corner[1] + move[1] <= 7:
                        if board[corner[0] + move[0]][corner[1] + move[1]] == my_color:
                            c -= 12.5
                        elif board[corner[0] + move[0]][corner[1] + move[1]] == op_color:
                            c += 12.5
                        else:
                            c = 0
                else:
                    if board[corner[0]][corner[1]] == my_color:
                        c += 25
                    else:
                        c -= 25

        my_sigma_value = 0
        my_square = board.get_squares(my_color)
        for x, y in my_square:
            my_sigma_value += self.BOARD_VALUE[x][y]

        op_sigma_value = 0
        op_square = board.get_squares(op_color)
        for x, y in op_square:
            op_sigma_value += self.BOARD_VALUE[x][y]

        # expected_move_value_for_my_color is the number of possible moves
        expected_move_value_for_my_color = len(board.get_legal_moves(my_color))

        return my_sigma_value - op_sigma_value + expected_move_value_for_my_color + p + c

    def _get_minimax_value(self, board, color, move, depth):
        """ Return the value of minimax for move. """

        # Create a deepcopy of the board to preserve the state of the actual board
        next_board = deepcopy(board)
        if move != (-1, -1):
            next_board.execute_move(move, color)
        next_color = color * -1

        # Limit depth of search to control time rule
        if depth >= self.STATIC_MAX_DEPTH:
            return self._get_heuristics_value(next_board)

        next_moves = board.get_legal_moves(next_color)
        if not next_moves:
            check_end_moves = board.get_legal_moves(color)
            if not check_end_moves:
                # every one cannot move, game over
                return self._get_heuristics_value(board, game_over=True)
            # this turn cannot move
            return self._get_minimax_value(next_board, next_color, (-1, -1), depth + 1)

        max_value = -self.MAX_VALUE
        # if this turn is my turn, try to max value for moves, else min value
        mark = 1 if next_color == self.my_color else -1

        # search next turn
        for possible_next_move in next_moves:
            next_value = mark * self._get_minimax_value(next_board, next_color, possible_next_move, depth + 1)
            if next_value > max_value:
                max_value = next_value

        return mark * max_value

    # def _get_minimax_alphabeta_value(self, board, color, move, alpha, bate, depth):
    #     """ minimax with alphabeta """
    #
    #     # Create a deepcopy of the board to preserve the state of the actual board
    #     next_board = deepcopy(board)
    #     if move != (-1, -1):
    #         next_board.execute_move(move, color)
    #     next_color = color * -1
    #
    #     # Limit depth of search to control time rule
    #     if depth >= self.STATIC_MAX_DEPTH:
    #         return self._get_heuristics_value(next_board)
    #
    #     next_moves = board.get_legal_moves(next_color)
    #     if not next_moves:
    #         check_end_moves = board.get_legal_moves(color)
    #         if not check_end_moves:
    #             # every one cannot move, game over
    #             return self._get_heuristics_value(board, game_over=True)
    #         # this turn cannot move
    #         return self._get_minimax_value(next_board, next_color, (-1, -1), depth + 1)
    #
    #     max_value = -self.MAX_VALUE
    #     # if this turn is my turn, try to max value for moves, else min value
    #     mark = 1 if next_color == self.my_color else -1
    #
    #     # search next turn
    #     for possible_next_move in next_moves:
    #         next_value = mark * self._get_minimax_value(next_board, next_color, possible_next_move, depth + 1)
    #         if next_value > max_value:
    #             max_value = next_value
    #     return mark * max_value


engine = StudentEngine
