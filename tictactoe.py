"""
Tic Tac Toe Player
"""

# Project assigned by: https://cs50.harvard.edu/ai/2024/projects/0/tictactoe/
# also checked code against this Medium post, which was very helpful: https://medium.com/analytics-vidhya/minimax-algorithm-in-tic-tac-toe-adversarial-search-example-702c7c1030eb
import math
import pdb
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    # """
    # Returns player who has the next turn on a board.
    # """
    count_of_x = 0
    count_of_o = 0

    if terminal(board):
        return None


    for row in board:
        for space in row:
            if space == X:
                count_of_x += 1
            elif space == O:
                count_of_o += 1

    if count_of_x > count_of_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # find where it says empty
    actions_can_take = set()

    # iterate through indices
    for index_row, row in enumerate(board):
        for index_space, space in enumerate(row):
            if space == EMPTY:
                actions_can_take.add(tuple((index_row, index_space)))
    
    return actions_can_take


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    row = action[0]
    space = action[1]
    current_player = player(board)
    board_copy = copy.deepcopy(board)

    # modify original board each time
    if board_copy[row][space] != EMPTY:
        raise Exception('Action not possible')

    else:
        board_copy[row][space] = current_player
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    count_of_x = 0
    count_of_o = 0
    # checks each row
    for row in board:
        for space in row:
            if space == X:
                count_of_x += 1
            elif space == O:
                count_of_o += 1

            if count_of_o == 3:
                return O
            elif count_of_x == 3:
                return X

        count_of_x = 0
        count_of_o = 0

    # checks up and down
    row = 0
    column = 0

    while column <= 2:
        while row <= 2:

            space = board[row][column]
            if space == X:
                count_of_x += 1
            elif space == O:
                count_of_o += 1

            if count_of_o == 3:
                return O
            if count_of_x == 3:
                return X

            row += 1

        column += 1
        # reset row
        row = 0
        count_of_o = 0
        count_of_x = 0

    # check diagonally
    # row and col increase
    if (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]) and board[1][1] != EMPTY:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # first check to see if someone has won the game
    if winner(board) != None:
        return True

    # check for tie
    for row in board:
        for space in row:
            if space == EMPTY:
                return False

    # if not empty spaces and no winner, there is a tie. return True-game is over.
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    winner_of_game = winner(board)
    if winner_of_game == X:
        return 1
    elif winner_of_game == O:
        return -1
    else:
        return 0

 # chooses the max val of all the possible mins
 # inspired by pseudo code here: https://cs50.harvard.edu/ai/2024/notes/0/
def max_value(board):
    # worst scenario is max value is -inf
    max_val = float('-inf')
    if terminal(board):
        return utility(board)

    for action in actions(board):
        resulting_board = result(board, action)
        max_val = max(max_val, min_value(resulting_board))

    return max_val

# chooses best min value of possible maxes
# inspired by pseudo code here: https://cs50.harvard.edu/ai/2024/notes/0/
def min_value(board):
    # worst scenario is min value is inf
    min_val = float('inf')
    if terminal(board):
        return utility(board)

    for action in actions(board):
        resulting_board = result(board, action)
        min_val = min(min_val, max_value(resulting_board))

    return min_val

# returns best action to take for maximizing player (X)
def minimax(board):
    # comment below if from Harvard CS-50 Into to AI course
    # The maximizing player picks action a in 
    # Actions(s) that produces the highest value of Min-Value(Result(s, a)).
    # The minimizing player picks action a in Actions(s) that produces the 
    # lowest value of Max-Value(Result(s, a)).

    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    current_player = player(board)
    best_action = None

    if current_player == X:
        max_val = float('-inf')
        for action in actions(board):
            resulting_board = result(board, action)

            # get min val
            min_val = min_value(resulting_board)

            # compare min to current max val. set max to highest min found.
            if min_val > max_val:
                max_val = min_val
                best_action = action

    elif current_player == O:
        min_val = float('inf')
        for action in actions(board):
            resulting_board = result(board, action)
            max_val = max_value(resulting_board)

            # if lower max val available, assign it to min.
            if max_val < min_val:
                min_val = max_val
                best_action = action

    return best_action
