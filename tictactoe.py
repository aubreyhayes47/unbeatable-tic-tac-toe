"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None

#Define Illegal Move Error
class IllegalMoveError(Exception):
    pass

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #Find number of moves each player has already taken
    xCount = 0
    oCount = 0
    for row in board:
        for i in range(3):
            if row[i] == X:
                xCount += 1
            elif row[i] == O:
                oCount += 1
    #X goes first so if xCount > oCount, return O
    #Else return X
    if xCount == 0 and oCount == 0:
        return X
    elif xCount > oCount:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #Initialize set of moves
    moves = set()
    
    #Calculate possible boards for that player
    #For each empty space, save that as a move before continuing to the next space
    for i,row in enumerate(board):
        for j in range(3):
            if row[j] == EMPTY:
                moves.add((i, j))
                        
    #Return the moves set
    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #Make a deep copy of the board and modify that
    #A regular assignment would change the original board and a shallow copy would change the rows of the original board
    newBoard = deepcopy(board)
    space = newBoard[action[0]][action[1]]

    #Raise exception for illegal moves
    if space != EMPTY:
        raise IllegalMoveError

    #Update the newBoard with the currPlayer and return the newBoard
    thisPlayer = player(newBoard)
    newBoard[action[0]][action[1]] = thisPlayer

    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Find if any row is fully populated by either player
    for row in board:
        if row[0] == X and row[1] == X and row[2] == X:
            return X
        elif row[0] == O and row[1] == O and row[2] == O:
            return O

    #Find if any column is fully populated by either player
    for i in range(3):
        if board[0][i] == X and board[1][i] == X and board[2][i] == X:
            return X
        elif board[0][i] == O and board[1][i] == O and board[2][i] == O:
            return O
    
    #Find if any diagonal is fully populated by either player
    #Check for each player
    for currPlayer in [X, O]:
        #Diagonal winner will always have the middle space
        if board[1][1] != currPlayer:
            continue
        #Check each pair of corners for the currPlayer
        elif (board[0][0] == currPlayer and board[2][2] == currPlayer) or (board[0][2] == currPlayer and board[2][0] == currPlayer):
            return currPlayer
    
    #If no winner was found, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #A winner being present means game over
    if winner(board):
        return True
    
    #If there was no winner and there is an empty space, game is not over
    for row in board:
        for i in range(3):
            if row[i] == EMPTY:
                return False
    
    #Otherwise, game over
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #It is assumed that only terminal boards will be passed into utility
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #If game over, return none
    if terminal(board):
        return None

    #Find out whose turn it is and all possible moves
    miniMaxPlayer = player(board)
    moves = actions(board)

    #Find and check the result of all possible moves for each player
    if miniMaxPlayer == X:
        #Set a placeholder for the winning score
        winningScore = -10
        
        #Iterate through all possible moves
        for move in moves:
            #Find the result and value of each move
            currResult = result(board, move)
            #Since we are trying to get the best move, we have to find the worst case scenario of each move
            #That worst-case is the actual 'value' of the move
            #To maximize, find the minvalue of each move
            moveValue = minValue(currResult) 
            if moveValue > winningScore:
                winningMove = deepcopy(move)
                winningScore = deepcopy(moveValue)
        return winningMove

    else:
        #Set a placeholder for the winning score
        winningScore = 10
        
        #Iterate through all possible moves
        for move in moves:
            #Find the result and value of each move
            currResult = result(board, move)
            #To minimize, find the max value of each move
            moveValue = maxValue(currResult) 
            if moveValue < winningScore:
                winningMove = deepcopy(move)
                winningScore = deepcopy(moveValue)
        return winningMove

def maxValue(board):
    #Any value will be higher than -10, so this is just a placeholder
    v = -10

    #If the board is over, return the score
    if terminal(board):
        return utility(board)

    #Find all possible moves
    possMoves = actions(board)

    #For each move, assign it a score of the worst possible end result
    for move in possMoves:
        moveResult = result(board,move)
        v = max(v, minValue(moveResult))
    return v

#The same function as maxValue, but finding the mininum
def minValue(board):
    v = 10
    if terminal(board):
        return utility(board)
    possMoves = actions(board)
    for move in possMoves:
        moveResult = result(board,move)
        v = min(v, maxValue(moveResult))
    return v