from engines import Engine
from copy import deepcopy


class StudentEngine(Engine):
    """ Game engine that you should you as skeleton code for your 
    implementation. """

    alpha_beta = False
    my_color = 0  # 1 = white, -1 = black

    MINIMAX_MAX_DEPTH = 2
    ALPHA_BETA_MAX_DEPTH = 2
    DYNAMIC_MAX_DEPTH = 3
    MAX_VALUE = 99999

    hash_dict = {}

    NODE_VISIT_NUMBER = 0
    NODE_HIT_NUMBER = 0

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
        self.my_color = color
        f = self.get_ab_minimax_move if self.alpha_beta else self.get_minimax_move
        return f(board, color, move_num, time_remaining, time_opponent)

    def get_minimax_move(self, board, color, move_num=None,
                         time_remaining=None, time_opponent=None):

        # Get a list of all legal moves.
        moves = board.get_legal_moves(color)

        if time_remaining > 15.0:
            count = board.count(color) + board.count(color * -1)
            if count % 2 == 1:
                count -= 1
            if count % 8 == 0:
                self.MINIMAX_MAX_DEPTH = self.DYNAMIC_MAX_DEPTH
        else:
            self.MINIMAX_MAX_DEPTH = 1

        # Return the best move according to max-min decision
        final_move = max(moves,
                         key=lambda move: self._get_minimax_value(board, self._hash_board(board), color, move, 0))
        print "minimax node number = ", self.NODE_VISIT_NUMBER, "hit number =", self.NODE_HIT_NUMBER
        return final_move

    def get_ab_minimax_move(self, board, color, move_num=None,
                            time_remaining=None, time_opponent=None):
        """ Skeleton code from greedy.py to get you started. """
        # Get a list of all legal moves.
        moves = board.get_legal_moves(color)

        # self.ALPHA_BETA_MAX_DEPTH = 2
        if time_remaining > 15.0:
            count = board.count(color) + board.count(color * -1)
            if count % 2 == 0:
                count -= 1
            if count % 8 == 0:
                self.ALPHA_BETA_MAX_DEPTH = 3
        else:
            self.ALPHA_BETA_MAX_DEPTH = 2

        # Return the best move according to our simple utility function:
        # which move yields the largest different in number of pieces for the
        # given color vs. the opponent?
        final_move = max(moves,
                         key=lambda move: self._get_minimax_alphabeta_value(board, self._hash_board(board), color, move,
                                                                            -self.MAX_VALUE, self.MAX_VALUE, 0))

        print "ab_minimax node number = ", self.NODE_VISIT_NUMBER, "hit number =", self.NODE_HIT_NUMBER
        return final_move

    def _hash_board(self, board):
        """ Too slow, need to update when minimax search """
        # hash_value = 0
        # white_squares = board.get_squares(1)
        # black_squares = board.get_squares(-1)

        # for x, y in white_squares:
        #     hash_value += x * 654377 + y * 35237
        # for x, y in black_squares:
        #     hash_value += x * 213123 + y * 32117
        hash_value = int(hash(board.toStr()))
        # board.display((10, 10))
        # print "hash value = ", hash_value
        return hash_value

    def _get_heuristics_value(self, board, next_board_hash, game_over=False):
        """ Calculate heuristics value for my color in board
            H(Board) =
                sigma(square_value) | all square in my color
              - sigma(square_value) | all square in opponent's color
              + expected_move_value_for_my_color
        """

        self.NODE_VISIT_NUMBER += 1

        # hash_value = self._hash_board(board)
        hash_value = next_board_hash
        if hash_value in self.hash_dict:
            self.NODE_HIT_NUMBER += 1
            return self.hash_dict[hash_value]

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

        my_sigma_value = 0
        my_square = board.get_squares(my_color)
        for x, y in my_square:
            my_sigma_value += self.BOARD_VALUE[x][y]

        op_sigma_value = 0
        op_square = board.get_squares(op_color)
        for x, y in op_square:
            op_sigma_value -= self.BOARD_VALUE[x][y]

        # expected_move_value_for_my_color is the number of possible moves

        expected_move_value_for_my_color = len(board.get_legal_moves(my_color))

        expected_move_value_for_op_color = len(board.get_legal_moves(op_color))
        # debug the heuristics_value
        # if self.NODE_NUMBER < 10:
        #     board.display((10, 10))
        #     print "my_sigma_value", my_sigma_value, \
        #         "op_sigma_value", op_sigma_value, \
        #         "expected_move_value_for_my_color", expected_move_value_for_my_color, \
        #         my_sigma_value - op_sigma_value + expected_move_value_for_my_color
        # parity
        my_count = board.count(my_color)
        op_count = board.count(op_color)
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
            for move in [(0, 1), (0, -1), (1, 0), (-1, 0),(-1, -1),(1,1),(-1, 1), (1, -1)]:
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
                        # 10
        heuristics_value = (my_sigma_value - op_sigma_value) * 20 + (expected_move_value_for_my_color - expected_move_value_for_op_color) * 10 + p * 10 + c * 2
        self.hash_dict[hash_value] = heuristics_value
        return heuristics_value

    def _update_board_hash(self, board, next_board, board_hash, color, move):
        next_board_hash = board_hash
        if color == 1:
            sx = 654377
            sy = 35237
            tx = 213123
            ty = 32117
        else:
            tx = 654377
            ty = 35237
            sx = 213123
            sy = 32117

        for x in range(8):
            for y in range(8):
                if board[x][y] != next_board[x][y]:
                    if board[x][y] != color:
                        if board[x][y] == 0:
                            # Empty, plus a new color one
                            next_board_hash += (x * sx + y * sy)
                        else:
                            # Flip, plus a new color one, subs a old color one
                            # next_board_hash -= (x * tx + y * ty)
                            # next_board_hash += (x * sx + y * sy)
                            # print next_board_hash, " ", x, " ", y
                            next_board_hash += (x * (sx - tx) + y * (sy - ty))

        return next_board_hash

    def _get_minimax_value(self, board, board_hash, color, move, depth):
        """ Return the value of minimax for move. """

        # Create a deepcopy of the board to preserve the state of the actual board
        next_board = deepcopy(board)
        next_board_hash = board_hash
        if move != (-1, -1):
            next_board.execute_move(move, color)
            # next_board_hash = self._update_board_hash(board, next_board, board_hash, color, move)
            next_board_hash = int(hash(board.toStr()))
        next_color = color * -1

        # if this turn is my turn, try to max value for moves, else min value
        mark = 1 if color == self.my_color else -1

        # Limit depth of search to control time rule
        if depth >= self.MINIMAX_MAX_DEPTH:
            return mark * self._get_heuristics_value(next_board, next_board_hash)

        next_moves = board.get_legal_moves(next_color)
        if not next_moves:
            check_end_moves = board.get_legal_moves(color)
            if not check_end_moves:
                # every one cannot move, game over
                return mark * self._get_heuristics_value(board, next_board_hash, game_over=True)
            # this turn cannot move
            return -self._get_minimax_value(next_board, next_board_hash, next_color, (-1, -1), depth + 1)

        max_value = -self.MAX_VALUE

        # search next turn
        for possible_next_move in next_moves:
            next_value = -self._get_minimax_value(next_board, next_board_hash, next_color, possible_next_move,
                                                  depth + 1)
            if next_value > max_value:
                max_value = next_value

        # board.display((10, 10))
        # print "color", color, "move", move, "depth", depth, "value", max_value
        return max_value

    def _get_minimax_alphabeta_value(self, board, board_hash, color, move, alpha, beta, depth):
        """ minimax with alphabeta """

        # Create a deepcopy of the board to preserve the state of the actual board
        next_board = deepcopy(board)
        next_board_hash = board_hash
        if move != (-1, -1):
            next_board.execute_move(move, color)
            # next_board_hash = self._update_board_hash(board, next_board, board_hash, color, move)
            next_board_hash = int(hash(board.toStr()))
        next_color = color * -1

        # if this turn is my turn, try to max value for moves, else min value
        mark = 1 if color == self.my_color else -1

        # Limit depth of search to control time rule
        if depth >= self.ALPHA_BETA_MAX_DEPTH:
            return mark * self._get_heuristics_value(next_board, next_board_hash)

        next_moves = board.get_legal_moves(next_color)
        if not next_moves:
            check_end_moves = board.get_legal_moves(color)
            if not check_end_moves:
                # every one cannot move, game over
                return mark * self._get_heuristics_value(board, next_board_hash, game_over=True)
            # this turn cannot move
            return -self._get_minimax_alphabeta_value(next_board, next_board_hash, next_color, (-1, -1), -beta, -alpha,
                                                      depth + 1)

        max_value = -self.MAX_VALUE

        # search next turn
        for possible_next_move in next_moves:
            next_value = -self._get_minimax_alphabeta_value(next_board, next_board_hash, next_color, possible_next_move,
                                                            -beta, -alpha, depth + 1)
            if next_value > alpha:
                alpha = next_value
                # meet the alpha beta pruning
                if alpha >= beta:
                    return next_value
            if next_value > max_value:
                max_value = next_value
        return max_value


engine = StudentEngine
