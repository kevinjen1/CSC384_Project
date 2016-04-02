from reversi_structure import *
from gtbase import *
from Hfunc import *
from Hfunc_old import *

initial_board = [[0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,'B','W',0,0,0],
                 [0,0,0,'W','B',0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0]]

initial_board_2 = [[0, 0, 0, 0, 0, 0, 0, 0],
                    ['B', 0, 0, 'W', 0, 0, 0, 0],
                     [0, 'B', 'W', 'W', 'B', 0, 0, 0],
                     [0, 0, 'W', 'B', 'B', 0, 0, 0],
                     [0, 'W', 'B', 'B', 'B', 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]


human = False
lines = "--------------------------------------------------"

board = ReversiBoard('Initial', initial_board)
top_node = GameTreeNode(board, None)

cur_node = top_node
cur_node.generateChildNodes()
i = 1
while not cur_node.getIfTerminal():
    print("Turn {} White".format(i))
    if len(cur_node.getChildrenWhite()) != 0:
        print("Searching for White")
        search_obj = GameTreeSearch(3,3)
        cur_node = search_obj.search(cur_node, 1, False, Hfunc)
        cur_board_object = cur_node.getReversiBoardObject()
        cur_board = cur_node.getBoardCopy()
        cur_board_object.printBoard()
        print(lines)
    print("Turn {} Black".format(i))
    if len(cur_node.getChildrenBlack()) != 0:
        if human == True:
            validMove = False
            while validMove == False:
                play = input('Human Move:')
                play = play.split(',')
                x = int(play[0])
                y = int(play[1])
                validMove = cur_node.checkMoveValidAndPerform('B', x, y, cur_board)
                if validMove == False:
                    print('INVALID MOVE')
            cur_board_object = ReversiBoard('Turn {}'.format(i),cur_board)
            cur_node = GameTreeNode(cur_board_object,cur_node)
            cur_board_object.printBoard()
            print(lines)
        else:
            print("Searching for MIN")
            search_obj = GameTreeSearch(3,3)
            cur_node = search_obj.search(cur_node, -1, False, Hfunc_old)
            cur_board_object = cur_node.getReversiBoardObject()
            cur_board = cur_node.getBoardCopy()
            cur_board_object.printBoard()
            print(lines)
    i = i + 1
    cur_node.generateChildNodes()

if cur_board_object.getScoreWhite() > cur_board_object.getScoreBlack():
    print("Game Over! White wins!")
else:
    print("Game Over! Black wins!")

