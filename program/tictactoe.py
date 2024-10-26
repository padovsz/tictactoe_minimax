import math

# Variables
X = 'X'
O = 'O'
EMPTY = None

# Initializes the deafult state of the board (all empty)
def initial_state():
    '''
    returns starting state of the board.
    '''
    return [[EMPTY for _ in range(3)] for _ in range(3)]

# Knowing that X always starts, we can just count the amount of Xs and Os, and with that we know who has to play next
def player(board):
    '''
    returns player who has the next turn on a board.
    '''
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)
    
    # if 'X' played less than or equal to 'O', it is 'X's turn, otherwise, it is 'O's turn
    return 'X' if x_count <= o_count else 'O'

# Checks all the spaces in the board and returns every empty one as a valid action
def actions(board):
    '''
    returns set of all possible actions (i, j) available on the board.
    '''
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

# Creates a copy of the board and adds the player action to it, then returns it
def result(board, action):
    '''
    returns the board that results from making move (i, j) on the board.
    '''
    p = player(board)
    i, j = action
    
    new_board = [row.copy() for row in board]
    new_board[i][j] = p
    
    return new_board

# Checks all the conditions for the win, and returns it if there's one
def winner(board):
    '''
    returns the winner of the game, if there is one.
    '''
    # check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not EMPTY:
            return board[0][j]

    # check diagonals 
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    # if no winner
    return None

# Simply checks if the game has finished wiht a True of False.
def terminal(board):
    '''
    returns True if game is over, False otherwise.
    '''
    if winner(board) is not None:
        return True
    
    for row in board:
        if EMPTY in row:
            return False 

    # the game is over (tie)
    return True

# The values for the minmax function.
def utility(board):
    '''
    returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    '''
    win = winner(board)
    
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

# Function that determines the best action possible, calculating the max_value of a play (the best possible one) thinking
# That the other side is trying to minimize your play after it
def minimax(board):
    if terminal(board): # Checks if the game has ended
        return None
    
    def max_value(board):  # Auxiliary Function that maximizes, starting from negative infinite.
        if terminal(board):
            return utility(board)
        v = float('-inf') # Lowest possible value
        for action in actions(board): # Checks all possible actions on the board
            v = max(v, min_value(result(board, action))) # If the new value is greater it is used instead
        return v

    def min_value(board): # Basically the same thing as the max_value but minimizes
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v
    
    current_player = player(board)
    
    if current_player == 'X':
        # X is the maximizer
        best_value = float('-inf')
        best_action = None
        
        for action in actions(board):
            # Get the new board state after the action
            new_board = result(board, action)
            
            # Check if this action leads to an immediate victory
            if terminal(new_board):
                if utility(new_board) == 1:  # X wins
                    return action  # Immediate win, return this action
            
            # If no immediate win, evaluate the board deeper
            value = min_value(new_board)
            if value > best_value:
                best_value = value
                best_action = action
                
        return best_action
    
    else:
        # O is the minimizer
        best_value = float('inf')
        best_action = None
        
        for action in actions(board):
            new_board = result(board, action)
            
            # Check if this action leads to an immediate victory
            if terminal(new_board):
                if utility(new_board) == -1:  # O wins
                    return action  # Immediate win, return this action
            
            value = max_value(new_board)
            if value < best_value:
                best_value = value
                best_action = action
                
        return best_action
