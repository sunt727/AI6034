# MIT 6.034 Lab 3: Games
# Written by 6.034 staff

from game_api import *
from boards import *
from toytree import GAME1

INF = float('inf')

# Please see wiki lab page for full description of functions and API.

#### Part 1: Utility Functions #################################################


def is_game_over_connectfour(board):
    """Returns True if game is over, otherwise False."""
    if board.count_pieces(current_player=None) == board.num_cols * board.num_rows:
        return True

    for s in board.get_all_chains():
        if len(s) >= 4:
            return True
    return False

    raise NotImplementedError


def next_boards_connectfour(board):
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    list_connectfour = []
    if is_game_over_connectfour(board):
        return list_connectfour

    for c in range(board.num_cols):
        if not board.is_column_full(c):
            list_connectfour.append(board.add_piece(c))
    return list_connectfour

    raise NotImplementedError


def endgame_score_connectfour(board, is_current_player_maximizer):
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    is_tie = True

    if is_game_over_connectfour(board):
        for s in board.get_all_chains():
            if len(s) >= 4:
                is_tie = False

        if is_tie:
            return 0
        else:
            return 1000 if not is_current_player_maximizer else -1000

    raise NotImplementedError

def endgame_score_connectfour_faster(board, is_current_player_maximizer):
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""

    return (board.num_cols * board.num_rows - board.count_pieces(None)) * \
           endgame_score_connectfour(board, is_current_player_maximizer)

    raise NotImplementedError


def heuristic_connectfour(board, is_current_player_maximizer):
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer.

    500 for a board in which the maximizer is doing much better
    10 for a board in which the maximizer is doing only slightly better
    0 for a board in which neither player seems to have an advantage
    -10 for a board in which the minimizer is doing slightly better
    ...and so on.
    """
    current_chain = []
    other_chain = []

    def heuristic_return():
        if max(current_chain) > max(other_chain):
            return 500
        elif max(current_chain) == max(other_chain):
            if current_chain.count(max(current_chain)) > other_chain.count(max(other_chain)):
                return 10
            elif current_chain.count(max(current_chain)) == other_chain.count(max(other_chain)):
                return 0
            else:
                return -10
        else:
            return -500

    if not is_game_over_connectfour(board):
        for c in board.get_all_chains(True):
            current_chain.append(len(c))
        for c in board.get_all_chains(False):
            other_chain.append(len(c))

    if is_current_player_maximizer:
        return heuristic_return()
    else:
        return -(heuristic_return())

    raise NotImplementedError

# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster,)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### Part 2: Searching a Game Tree #############################################

# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""

    if state.is_game_over():
        leaf_score = state.get_endgame_score()
        return([state], leaf_score, 1)

    static_eval = 0
    best_score = -INF
    next_states = state.generate_next_states()

    for next_state in next_states:
        (path, score, evalution) = dfs_maximizing(next_state)
        static_eval += evalution
        if score > best_score:
            best_score = score
            best_path = [state] + path

    return (best_path, best_score, static_eval)

    raise NotImplementedError


# Uncomment the line below to try your dfs_maximizing on an
# AbstractGameState representing the games tree "GAME1" from toytree.py:

# pretty_print_dfs_type(dfs_maximizing(GAME1))


def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""

    def max_value(state):

        best_path = [state]

        if state.is_game_over():
            leaf_score = state.get_endgame_score(True)
            return (best_path, leaf_score, 1)

        static_eval = 0
        best_score = -INF
        next_states = state.generate_next_states()

        for next_state in next_states:
            (path, score, evalution) = min_value(next_state)
            static_eval += evalution
            if best_score < score:
                best_score = score
                best_path = [state] + path

        return (best_path, best_score, static_eval)

    def min_value(state):

        best_path = [state]

        if state.is_game_over():
            leaf_score = state.get_endgame_score(False)
            return (best_path, leaf_score, 1)

        static_eval = 0
        best_score = +INF
        next_states = state.generate_next_states()

        for next_state in next_states:
            (path, score, evalution) = max_value(next_state)
            static_eval += evalution
            if best_score > score:
                best_score = score
                best_path = [state] + path

        return (best_path, best_score, static_eval)


    return max_value(state) if maximize else min_value(state)

    raise NotImplementedError


# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

# pretty_print_dfs_type(minimax_endgame_search(GAME1, True))
# pretty_print_dfs_type(minimax_endgame_search(GAME1, False))
# pretty_print_dfs_type(minimax_endgame_search(NEARLY_OVER))


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True):
    """Performs standard minimax search. Same return type as dfs_maximizing."""

    def max_value(state, depth):

        best_path = [state]

        if state.is_game_over():
            leaf_score = state.get_endgame_score(True)
            return (best_path, leaf_score, 1)
        elif depth == 0:
            leaf_score = heuristic_fn(state.get_snapshot(), True)
            return (best_path, leaf_score, 1)

        static_eval = 0
        best_score = -INF
        next_states = state.generate_next_states()

        for next_state in next_states:
            (path, score, evalution) = min_value(next_state, depth-1)
            static_eval += evalution
            if best_score < score:
                best_score = score
                best_path = [state] + path

        return (best_path, best_score, static_eval)

    def min_value(state,depth):

        best_path = [state]

        if state.is_game_over():
            leaf_score = state.get_endgame_score(False)
            return (best_path, leaf_score, 1)
        elif depth == 0:
            leaf_score = heuristic_fn(state.get_snapshot(), False)
            return (best_path, leaf_score, 1)

        static_eval = 0
        best_score = +INF
        next_states = state.generate_next_states()

        for next_state in next_states:
            (path, score, evalution) = max_value(next_state, depth-1)
            static_eval += evalution
            if best_score > score:
                best_score = score
                best_path = [state] + path

        return (best_path, best_score, static_eval)


    return max_value(state, depth_limit) if maximize else min_value(state, depth_limit)

    raise NotImplementedError


# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1. Try increasing the value of depth_limit to see what happens:

#pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    """"Performs minimax with alpha-beta pruning. Same return type 
    as dfs_maximizing."""


    def max_value(state, depth, alpha, beta):

        best_path = [state]

        if state.is_game_over():
            leaf_score = state.get_endgame_score(True)
            return (best_path, leaf_score, 1)
        elif depth == 0:
            leaf_score = heuristic_fn(state.get_snapshot(), True)
            return (best_path, leaf_score, 1)
        elif alpha >= beta:
            return None

        static_eval = 0
        best_score = -INF
        next_states = state.generate_next_states()

        for next_state in next_states:
            (path, score, evalution) = min_value(next_state, depth-1, alpha, beta)
            static_eval += evalution
            if best_score < score:
                best_score = score
                if alpha < best_score:
                    alpha = best_score
                    if alpha >= beta:
                        return (best_path, best_score, static_eval)
                best_path = [state] + path

        return (best_path, best_score, static_eval)

    def min_value(state,depth, alpha, beta):

        best_path = [state]

        if state.is_game_over():
            leaf_score = state.get_endgame_score(False)
            return (best_path, leaf_score, 1)
        elif depth == 0:
            leaf_score = heuristic_fn(state.get_snapshot(), False)
            return (best_path, leaf_score, 1)
        elif alpha >= beta:
            return None

        static_eval = 0
        best_score = +INF
        next_states = state.generate_next_states()

        for next_state in next_states:
            (path, score, evalution) = max_value(next_state, depth-1, alpha, beta)
            static_eval += evalution
            if best_score > score:
                best_score = score
                if beta > best_score:
                    beta = best_score
                    if alpha >= beta:
                        return (best_path, best_score, static_eval)
                best_path = [state] + path

        return (best_path, best_score, static_eval)


    return max_value(state, depth_limit, alpha, beta) if maximize else min_value(state, depth_limit, alpha, beta)


    raise NotImplementedError


# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4. Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

# pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""


    anytime = AnytimeValue()

    for d in range(depth_limit):

        new_best_option = minimax_search_alphabeta(state, alpha=-INF, beta=INF, depth_limit=d+1, maximize=maximize, \
                                                   heuristic_fn=heuristic_fn)

        anytime.set_value(val=new_best_option)

    return anytime.copy()

    raise NotImplementedError


# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4. Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

# progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4).pretty_print()


# Progressive deepening is NOT optional. However, you may find that 
#  the tests for progressive deepening take a long time. If you would
#  like to temporarily bypass them, set this variable False. You will,
#  of course, need to set this back to True to pass all of the local
#  and online tests.
TEST_PROGRESSIVE_DEEPENING = True
if not TEST_PROGRESSIVE_DEEPENING:
    def not_implemented(*args): raise NotImplementedError
    progressive_deepening = not_implemented


#### Part 3: Multiple Choice ###################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'


#### SURVEY ###################################################

NAME = 'Tuo Sun'
COLLABORATORS = 'Sen Dai'
HOW_MANY_HOURS_THIS_LAB_TOOK = 10
WHAT_I_FOUND_INTERESTING = 'Good note on webpage'
WHAT_I_FOUND_BORING = 'None'
SUGGESTIONS = None
