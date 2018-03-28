"""
Mark Klobukov
Chess Move Validation Engine for CS 576
9/1/2017
"""
from __future__ import print_function
import string
import numpy as np


BOARD_SIZE = 8
PROMPT_INPUT = True

MOVE_VECTORS = {'k' : [[0, 1], [1, 0], [-1, 0], [0, -1], [-1, -1], [1, -1], [-1, 1], [1, 1]],
                'q' : [[0, 1], [1, 0], [-1, 0], [0, -1], [-1, -1], [1, -1], [-1, 1], [1, 1]],
                'p' : [[1, 0]],
                'n' : [[2, -1], [2, 1], [1, 2], [1, -2], [-2, 1], [-2, -1], [-1, -2], [-1, 2]],
                'b' : [[1, 1], [-1, -1], [1, -1], [-1, 1]],
                'r' : [[0, 1], [1, 0], [0, -1], [-1, 0]]
               }

MOVE_DIST = {'k' : 1,
             'q' : BOARD_SIZE-1,
             'p' : 1,
             'n' : 1,
             'b' : BOARD_SIZE-1,
             'r' : BOARD_SIZE-1
            }

WHITE_PIECES = []
BLACK_PIECES = []

NUMBER_TO_LETTER_MAP = dict(enumerate(string.ascii_lowercase, 0))

def inBounds(xCoord, yCoord):
    """
    Checks whether a given square is in board bounds
    Args:
        param1: x coordinate
        param2: y coordinate

    Returns:
        True if square is in bounds
        False otherwise
    """
    return bool(xCoord < BOARD_SIZE and yCoord < BOARD_SIZE and xCoord >= 0 and yCoord >= 0)


def promptConfiguration(color):
    """
    Asks user for a given color configuration

    Args:
        param1: color of the chess pieces

    Returns:
        List of individual pieces configurations
    """
    inp = str(input(color + " configuration: "))
    inp = "".join(inp.split())
    configList = inp.split(",")
    return configList

def separateConfigIntoList(configStr):
    outList = "".join(configStr.split())
    outList = outList.split(",")
    return outList

def createPiece(color, config):
    """
    Creates a Piece object with provided color and configuration
    Assuming config is in the form Rf1, Kg1, etc...

    Args:
        param1: Color string. black or white
        param2: Config of the individual piece, e.g. "Kg8"
    """

    pieceType = config[0]
    posHoriz = letterToNumber(config[1])
    posVert = config[2]
    thisPiece = Piece(config, color, pieceType, [int(posVert)-1, int(posHoriz)])
    return thisPiece

def configToPosition(config):
    posHoriz = int(letterToNumber(config[0]))
    posVert = int(config[1])
    return [posVert, posHoriz]

def parseConfigurations(configList, color):
    """
    Populates the global arrays containing white and black pieces

    Args:
        param1: List of configurations returned by promptConfiguration function
        param2: color string. white or black
    Returns:
        Returns list of piece object.
    """
    pieceList = list()
    for config in configList:
        newPiece = createPiece(color, config.lower())
        pieceList.append(newPiece)

    return pieceList

def initBoard(whitePieces, blackPieces):
    """
    Places pieces on the board

    Args:
        param1: list of white pieces objects
        param2: list of black pieces objects

    Returns:
        two-dimensional list of pieces, placed according
        to individual configurations
    """
    board = [[None for xCoord in range(BOARD_SIZE)] for yCoord in range(BOARD_SIZE)]
    for piece in whitePieces:
        board[piece.pos[0]][piece.pos[1]] = piece
    for piece in blackPieces:
        board[piece.pos[0]][piece.pos[1]] = piece
    return board

def findPiece(piecesList, pieceConfig):
    """
    Finds a piece in the list by its config

    Args:
        param1: list of piece objects
        param2: configuration of the piece to find

    Returns:
        piece object with provided configuration or
        None if not found
    """
    for piece in piecesList:
        if piece.config == pieceConfig.lower():
            return piece
    return None

def isKingExposed(kingColor, board, blackPieces, whitePieces):
    """
    An important condition for move validity is that
    a given move not expose the king to a check. This
    function checks for this condition.

    Args:
        param1: color of the king (color of the player that makes a move)
        param2: board matrix
        param3: list of black pieces objects
        param4: list of white piecces objects

    Returns:
        True if a move exposes king to a check
        False otherwise
    """
    #for each of the pieces of opposite color
    #verify whether they do a check on the king
    attackerPieces = blackPieces
    if kingColor == "black":
        attackerPieces = whitePieces

    king = None
    if kingColor == "black":
        king = findKing(blackPieces)
    else:
        king = findKing(whitePieces)
    #compute all valid moves for a piece
    #if any of them happens to coincide with king's position
    #return True

    for piece in attackerPieces:
        #call listMoves with checkKing=False, checkForCheck=false to avoid infinite recursion
        allowedMoves = listMoves(piece.config, board, False, False, whitePieces, blackPieces)
        for move in allowedMoves:
            #print("Move and kingpos: ", move, np.array(king.pos))
            if np.array_equal(move, np.array(king.pos)):
                return True
    return False

def listMoves(pieceConfig, board, checkKing, checkForCheck, whitePieces, blackPieces):
    """
    Lists allowed moves for a given piece

    Args:
        param1: configuration of a piece to be moved
        param2: two-dimensional board matrix
        param3: boolean determining if the function should check
                whether a move exposes the king
        param4: boolean determining if the function should check
                whether the opponent's king is in check
        param5: list of white piece objects
        param6: list of black piece objects

    Returns:
        List of the allowed positions for the given piece to take
    """
    piece = findPiece(whitePieces, pieceConfig.lower())
    myColor = "white"
    if piece is None:
        piece = findPiece(blackPieces, pieceConfig.lower())
        myColor = "black"
        if piece is None:
            print("Piece with provided config not found. Exiting.")
            return

    #look up the piece's motion vectors dir and magnitude
    vecs = MOVE_VECTORS[piece.type]
    mag = MOVE_DIST[piece.type]
    posInit = piece.pos


    #check the special case - pawn
    if piece.type == 'p':
        allowedMoves = []
        allowedMoves = checkPawnMoves(myColor, board, posInit[0], posInit[1])
        return allowedMoves


    #for every direction
    #for every magnitude
    #increment pos by one and check:
        #fail conditions: oob, bump into own piece, expose king
        #success cond: kill opponent, land in empty spot.
            #add current spot and move on to next in magnitude
    allowedMoves = []
    pos = posInit

    for vec in vecs:
        #print("current vec: ", vec)
        for dist in range(1, mag+1):
            #increment pos by d
            increment = np.dot(vec, dist)
            pos = np.add(posInit, increment)
            #validate move returns two booleans
            #1) Move valid; 2) discontinue the loop
            moveValid, discontinue = validateMove(pos[0], pos[1], board, myColor,
                                                 blackPieces, whitePieces, checkKing, checkForCheck)
            if moveValid:
                allowedMoves.append(pos)
            if discontinue:
                break

    return allowedMoves

def checkPawnMoves(myColor, board, yCoord, xCoord):
    """
    Equivalent to the listMoves function except only applies to pawns
    The reason: pawns are a special case and their movement patterns
    do not conform to the general formula for the other pieces

    Args:
        param1: color of the player that is making a move
        param2: two-dim board matrix
        param3: vertical coordinate of pawn
        param4: horizontal coordinate of pawn

    Returns:
        List of allowed positions where the pawn can move.
    """
    pawnMoves = list()
    if myColor == "white":
        #move up
        if board[yCoord+1][xCoord] is None:
            pawnMoves.append([yCoord+1, xCoord])
            if str(yCoord) == str('1') and board[yCoord+2][xCoord] is None:
                pawnMoves.append([yCoord+2, xCoord])

        #check if the pawn can diagonally kill an opponent piece
        if inBounds(yCoord+1, xCoord-1) and board[yCoord+1][xCoord-1] != None:
            if board[yCoord+1][xCoord-1].color != myColor and board[yCoord+1][xCoord-1].type != 'k':
                pawnMoves.append([xCoord-1, yCoord+1])
        if inBounds(yCoord+1, xCoord+1) and board[yCoord+1][xCoord+1] != None:
            if board[yCoord+1][xCoord+1].color != myColor and board[yCoord+1][xCoord+1].type != 'k':
                pawnMoves.append([yCoord+1, xCoord+1])

    else: #if color black
        if board[yCoord-1][xCoord] is None:
            pawnMoves.append([yCoord-1, xCoord])
            if str(yCoord) == str('6') and board[yCoord-2][xCoord] is None:
                pawnMoves.append([yCoord-2, xCoord])
        if inBounds(yCoord-1, xCoord-1) and board[yCoord-1][xCoord-1] != None:
            if board[yCoord-1][xCoord-1].color != myColor and board[yCoord-1][xCoord-1].type != 'k':
                pawnMoves.append([yCoord-1, xCoord-1])
        if inBounds(yCoord-1, xCoord+1) and board[yCoord-1][xCoord+1] != None:
            if board[yCoord-1][xCoord+1].color != myColor and board[yCoord-1][xCoord+1].type != 'k':
                pawnMoves.append([yCoord-1, xCoord+1])
    return pawnMoves

def findKing(pieces):
    """
    Find the king in the pieces list

    Args:
        param1: list of piece objects for a given color

    Returns:
        King piece object if found
        None if not found (should not happen for valid configuration)
    """
    for piece in pieces:
        if piece.type.lower() == "k":
            return piece
    return None

def decodePosition(pos):
    """
    Translates position list into human-readable chess configuration

    Args:
        param1: position list in the form [y, x]

    Returns:
        Readable string such as g8 or a7
    """
    posOut = ""
    posOut += (str(NUMBER_TO_LETTER_MAP[pos[1]]) + str(pos[0]+1))
    return posOut

def createDecodedOutput(validMoves):
    """
    Creates a human-readable output of a list of positions

    Args:
        param1: list of moves

    Returns:
        String of comma-separated configuration like "g8, a7, c3"
    """
    decodedMoves = ""
    for move in validMoves:
        decodedMoves += decodePosition(move) + ", "
    return decodedMoves[0:len(decodedMoves)-2]

def getCheckedKingColor(board, blackPieces, whitePieces):
    """
    Check if either king is exposed
    to a check and return exposed king's color

    Args:
        param1: two-dimensional matrix of piece objects
        param2: list of black pieces objects
        param3: list of white pieces objects

    Returns:
        Boolean value for whether either king is exposed to check
        String indicating color of exposed king.

        If False is returned, the returned color string is empty
    """
    #find if either king is exposed
    #if so, allowed moves should only be returned
    #if the selected piece is the checked king
    kingInCheck = ""
    if isKingExposed("black", board, blackPieces, whitePieces):
        kingInCheck = "black"
    elif isKingExposed("white", board, blackPieces, whitePieces):
        kingInCheck = "white"

    if len(kingInCheck) > 0:
        return [True, kingInCheck]
    return [False, ""]

def canMoveWithACheckToOpponent(pieceToMoveColor, board, blackPieces, whitePieces):
    """
    Check whether the opponent's king is in check. If so,
    no move is valid and the program should exit

    Args:
        param1: color of the player that is making a move
        param2: two-dim matrix of pieces
        param3: list of black pieces
        param4: list of white pieces

    Returns:
        True if opponent's king in check
        False otherwise
    """
    checkResult = getCheckedKingColor(board, blackPieces, whitePieces)
    if checkResult[0] is True:
        #check if the opponent's king is in check.
        #if so, can't move my own pieces, print error
        if pieceToMoveColor != checkResult[1]:
            return False
    return True

#this func returns two boolean values: 1) moveValid, 2) stop checking
def validateMove(yCoord, xCoord, board, myColor, blackPieces, whitePieces, checkKing, checkForCheck):
    """
    Checks if a given move is valid for a piece

    Args:
        param1: config string for a piece to move
        param2: vertical coordinate of checked position
        param3: horizontal coordinate of checked position
        param4: two-dim matrix with piece objects
        param5: color of the player making move
        param6: list of black pieces
        param7: list of white pieces
        param8: boolean indicating whether to check if king gets exposed
        param9: boolean indicating whether to verify if there is a check

    Returns:
        bool1: whether the move is valid
        bool2: whether the program should keep checking moves for a given piece
    """
    #check if move is out of bounds or the opponent's king is in check.
    #if the latter is true, it doesn't make sense to continue move validation at all
    if not inBounds(xCoord, yCoord) or (checkForCheck and not canMoveWithACheckToOpponent(myColor, board, blackPieces, whitePieces)):
        return False, True

    #check if a given move exposes my king to a check - can't go there
    if checkKing and isKingExposed(myColor, board, blackPieces, whitePieces):
        return False, False

    #if kill opponent, take its spot and stop checking further:
    if board[yCoord][xCoord] != None:
        #if a piece hit a piece with same color, return false and signal to stop moving
        if sameColor(board, yCoord, xCoord, myColor):
            return False, True
        else:
            return True, True
    #if empty square, may keep going further

    return True, False

def sameColor(board, yCoord, xCoord, myColor):
    """
    Checks if the piece at a given position is same color as provided color

    Args:
        param1: two-dim matrix of piece objects
        param2: vertical coordinate
        param3: horizontal coordinate
        param4: color to compare to

    Returns:
        True if same color,
        False otherwise
    """
    if board[yCoord][xCoord] != None and board[yCoord][xCoord].color.lower() == myColor.lower():
        return True
    return False

def letterToNumber(letter):
    """
    Converts letter to its position in alphabet

    Args:
        param1: letter to convert

    Returns:
        Index of the letter in the alphabet
    """
    return string.ascii_lowercase.index(letter)

def promptPieceToMove():
    """
    Prompts user to enter configuration of the piece of be moveValid

    Args:
        None

    Returns:
        Piece configuration string directly from user input
    """
    return str(input("Piece to move: "))

class Piece(object):
    """
    Class representing any piece on the board

    Properties:
        Config: configuration like kg8 or bh4
        Type: piece name, such as 'k' for king or 'b' for bishop
        Color: white or black (string)
        Pos: position in the format [y, x]
    """
    def __init__(self, config, color, pieceType, pos):
        self.config = config
        self.type = pieceType
        self.color = color
        self.pos = pos
    def __str__(self):
        return "This piece: " + str(self.type) + str(self.color) + str(self.pos)

def main():
    """
    Main function. Executed from command line.
    Args:
        None

    Returns:
        None
    """
    whiteConfig = promptConfiguration("white")
    blackConfig = promptConfiguration("black")
    pieceToMove = promptPieceToMove()

    whitePieces = parseConfigurations(whiteConfig, "white")
    blackPieces = parseConfigurations(blackConfig, "black")

    board = initBoard(whitePieces, blackPieces)
    validMoves = listMoves(str(pieceToMove), board, True, True, whitePieces, blackPieces)
    res = ""
    res += "\nLEGAL MOVES FOR " + pieceToMove + ": "
    res += createDecodedOutput(validMoves)
    print(res)

if __name__ == "__main__":
    main()
