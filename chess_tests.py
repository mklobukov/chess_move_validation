from main import *
from collections import Counter
# #initialize a few pieces, piece lists, and boards
whiteConf1 = "Rf1, Kg1, Pf2, Ph2, Pg3"
blackConf1 = "Kb8, Ne8, Pa7, Pb7, Pc7, Ra5, Bf5"

whitePieces1 = parseConfigurations(separateConfigIntoList(whiteConf1), "white")
blackPieces1 = parseConfigurations(separateConfigIntoList(blackConf1), "black")
board1 = initBoard(whitePieces1, blackPieces1)

blackConf2 = "Kb7, Rc7, Rb6, Qc6, Nc5, Pb6, Pe6"
whiteConf2 = "Kd2, Pc3, Qe4, Pf3, Bf2, Rg1"
whitePieces2 = parseConfigurations(separateConfigIntoList(whiteConf2), "white")
blackPieces2 = parseConfigurations(separateConfigIntoList(blackConf2), "black")
board2 = initBoard(whitePieces2, blackPieces2)

whiteConf3 = "Pa2, Pb2, Nd2, Ke2, Pf2, Ph2, Pe3, Qd4, Ne5, Pc6"
blackConf3 = "Ra8, Kc8, Qa1, Bf8, ng8, Rh8, Pc7, Pe7, Pg7, Ph7, Pa6, Be6"
whitePieces3 = parseConfigurations(separateConfigIntoList(whiteConf3), "white")
blackPieces3 = parseConfigurations(separateConfigIntoList(blackConf3), "black")
board3 = initBoard(whitePieces3, blackPieces3)

#config 4 with a check
whiteConf4 = "Ka1, Rh7"
blackConf4 = "Ra8, Kg6, Pg5"
whitePieces4 = parseConfigurations(separateConfigIntoList(whiteConf4), "white")
blackPieces4 = parseConfigurations(separateConfigIntoList(blackConf4), "black")
board4 = initBoard(whitePieces4, blackPieces4)

#config5, also with a check to black king
whiteConf5 = "Rf1, Kg1, Pf2, Ph2, Pg3, Bf5"
blackConf5 = "Kc8, Re8, Pa7, Pb7, Pc7, Be8, Ra5"
whitePieces5 = parseConfigurations(separateConfigIntoList(whiteConf5), "white")
blackPieces5 = parseConfigurations(separateConfigIntoList(blackConf5), "black")
board5 = initBoard(whitePieces5, blackPieces5)

#test inBounds()
def test_inBounds():
    assert inBounds(0, 0) == True
    assert inBounds(8, 0) == False
    assert inBounds(-1, 5) == False
    assert inBounds(3, 3) == True
    assert inBounds(-1, -2) == False
    assert inBounds(9, 9) == False


def test_decodePosition():
    assert decodePosition([0, 1]) == "b1"
    assert decodePosition([5, 5]) == "f6"
    assert decodePosition([7, 6]) == "g8"

def test_createDecodedOutput():
    case1 = [[0, 1], [5, 5], [3, 6]]
    res1 = "b1, f6, g4"
    case2 = [[7, 0], [5, 0], [3, 2]]
    res2 = "a8, a6, c4"
    case3 = [[6, 1], [3, 3], [2, 7]]
    res3 = "b7, d4, h3"

    assert createDecodedOutput(case1) == res1
    assert createDecodedOutput(case2) == res2
    assert createDecodedOutput(case3) == res3

def test_letterToNumber():
    assert letterToNumber('a') == 0
    assert letterToNumber('z') == 25
    assert letterToNumber('c') == 2
    assert letterToNumber('h') == 7

def test_findPiece():
    """try finding Pf2 from config 1 white,
    Rc7 from config2 black
    Bf8 from config3 black"""

    Pf2 = Piece("Pf2", "white", "p", [1, 5])
    Rc7 = Piece("Rc7", "black", "r", [6, 2])
    Bf8 = Piece("Bf8", "black", "b", [7, 1])
    print(Pf2, Rc7, Bf8)
    assert findPiece(whitePieces1, "Pf2").config == 'pf2'
    assert findPiece(blackPieces2, "Rc7").config == 'rc7'
    assert findPiece(blackPieces3, "Bf8").config == 'bf8'

def test_isKingExposed():
    assert isKingExposed("white", board4, blackPieces4, whitePieces4) == True
    assert isKingExposed("black", board3, blackPieces3, whitePieces3) == False
    assert isKingExposed("white", board1, blackPieces1, whitePieces1) == False

def test_listMoves():
    #test king on board 2, pos d2
    board2_kd2 = ['e1', 'd1', 'c1', 'c2', 'd3', 'e3', 'e2']
    board2_kd2.sort()
    board2_kd2 = ", ".join(board2_kd2)
    moves = listMoves('kd2', board2, True, True, whitePieces2, blackPieces2)
    kd2 = list()
    for move in moves:
        kd2.append(decodePosition(move))
    kd2.sort()
    kd2 = ", ".join(kd2)
    assert kd2 == board2_kd2

    #test pawn on board 1, pos h2
    board1_ph2 = ['h3, h4']
    board1_ph2.sort()
    board1_ph2 = ", ".join(board1_ph2)

    moves = listMoves('ph2', board1, True, True, whitePieces1, blackPieces1)
    ph2 = list()
    for move in moves:
        ph2.append(decodePosition(move))
    ph2.sort()
    ph2 = ", ".join(ph2)
    assert ph2 == board1_ph2

    #test queen on board3, pos a1
    board3_qa1 = ['b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'b2', 'a2']
    board3_qa1.sort()
    board3_qa1 = ", ".join(board3_qa1)

    moves = listMoves('qa1', board3, True, True, whitePieces3, blackPieces3)
    qa1 = list()
    for move in moves:
        qa1.append(decodePosition(move))
    qa1.sort()
    qa1 = ", ".join(qa1)
    assert qa1 == board3_qa1

def test_canMoveWithACheckToOpponent():
    assert canMoveWithACheckToOpponent("white", board5, blackPieces5, whitePieces5) == False
    assert canMoveWithACheckToOpponent("black", board4, blackPieces4, whitePieces4) == False
    assert canMoveWithACheckToOpponent("white", board3, blackPieces3, whitePieces3) == True

def test_sameColor():
    assert sameColor(board5, 0, 6, "white") == True
    assert sameColor(board5, 4, 0, "white") == False

def test_getCheckedKingColor():
    assert getCheckedKingColor(board5, blackPieces5, whitePieces5) == [True,"black"]
    assert getCheckedKingColor(board1, blackPieces1, whitePieces1) == [False,""]

def test_findKing():
    kc8 = Piece('Kc8', 'black', 'k', [7, 2])
    assert findKing(blackPieces5).config.lower() == kc8.config.lower()
    kg1 = Piece('Kg1', 'white', 'k', [0, 6])
    assert findKing(whitePieces1).config.lower() == kg1.config.lower()
def main():
    whiteConf1 = "Rf1, Kg1, Pf2, Ph2, Pg3"
    blackConf1 = "Kb8, Ne8, Pa7, Pb7, Pc7, Ra5, Bf5"
    print(separateConfigIntoList(whiteConf1))
    whitePieces1 = parseConfigurations(separateConfigIntoList(whiteConf1), "white")
    print(whitePieces1)
    blackPieces1 = parseConfigurations(separateConfigIntoList(blackConf1), "black")
    board1 = initBoard(whitePieces1, blackPieces1)

    print (whitePieces1)

if __name__ == "__main__":
    main()
