from reversi_structure import *
from gtbase import *
from Hfunc import *

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

board = ReversiBoard('Initial', initial_board)
top_node = GameTreeNode(board, None)

cur_node = top_node
cur_node.generateChildNodes()
i = 0
while not cur_node.getIfTerminal():
    print("Next Move")
    if len(cur_node.getChildrenWhite()) != 0:
        print("Searching for MAX")
        search_obj = GameTreeSearch(0,6)
        cur_node = search_obj.search(cur_node, 1, True, Hfunc)
        cur_board_object = cur_node.getReversiBoardObject()
        cur_board = cur_node.getBoardCopy()
        cur_board_object.printBoard()
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
        else:
            print("Searching for MIN")
            search_obj = GameTreeSearch(0,5)
            cur_node = search_obj.search(cur_node, -1, True, Hfunc)
            cur_board_object = cur_node.getReversiBoardObject()
            cur_board = cur_node.getBoardCopy()
            cur_board_object.printBoard()
    cur_node.generateChildNodes()
print("Game Over!")

