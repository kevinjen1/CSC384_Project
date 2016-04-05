import copy

class ReversiBoard:
    '''
    Class to contain the Current state of the Reversi board. Holds the name of that board
    instance, the state of the board in a list of lists that represent the rows and columns
    of the board, the total number of black and white tokens on the board called score_black
    and score_white respectively.
    '''
    #Initialize the board
    def __init__(self, name, board):
        self.name = name
        self.board = board
        self.score_black = 0
        self.score_white = 0

        self.computeScoreBlack()
        self.computeScoreWhite()

    # Count the total number of black tokens on the board.
    def computeScoreBlack(self):
        for row in self.board:
            for cell in row:
                if cell == 'B':
                    self.score_black = self.score_black + 1
        return

    # Count the toatl number of white tokens on the board.
    def computeScoreWhite(self):
        for row in self.board:
            for cell in row:
                if cell == 'W':
                    self.score_white = self.score_white + 1
        return

    # Print the board and corresponding score of each colour of token.
    def printBoard(self):
        for row in self.board:
            print ('[%s]' % ', '.join(map(str, row)))
        print('    Score: W:{}, B:{}'.format(self.score_white,self.score_black))
        return

    # Return an instance of the board which should not be edited.
    def getBoard(self):
        return self.board

    # Return the number of black tokens on the board
    def getScoreBlack(self):
        return self.score_black

    # Return the number of white tokens on the board
    def getScoreWhite(self):
        return self.score_white

    # Return the name of the Board
    def getName(self):
        return self.name
class GameTreeNode:
    '''
    A object that contains a ReversiBoard object, an instance of the board from the ReversiBoard object,
    a boolean flag (isTerminal) that indicates if there is no children that can be created from the current node,
    a reference to the parent node, lists containing other GameTreeNodes that can be created by black and white moves.

    Note: For isTerminal to have a correct value, generateChildNodes must be called.
    '''
    def __init__(self, reversiBoard, parent):
        self.reversiBoardObject = reversiBoard
        self.nodeBoard = reversiBoard.getBoard()
        self.isTerminal = False
        self.parent = parent
        self.children_black = []
        self.children_white = []

    def __repr__(self):
        return self.reversiBoardObject.getName()

    # get the ReversiBoard object
    def getReversiBoardObject(self):
        return self.reversiBoardObject

    # Get a copy of the board that can be modified
    def getBoardCopy(self):
        return copy.deepcopy(self.nodeBoard)

    # Get all the children of the GameTreeNode
    def getChildren(self):
        all_children = []
        all_children.extend(self.children_black)
        all_children.extend(self.children_white)
        return all_children

    # Get all the children of the GameTreeNode that can be made by a black move
    def getChildrenBlack(self):
        return self.children_black

    # Get all the children of the GameTreeNode that can be made by a white move
    def getChildrenWhite(self):
        return self.children_white

    # Get if the GameTreeNode has children
    def getIfTerminal(self):
        return self.isTerminal

    # Check to see if a given move is valid, and if it is create the new board that
    # represents that move
    def checkMoveValidAndPerform(self, current_colour, x, y, board):
        moveSupported = False
        for x_inc, y_inc in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            if self.withinBoardScope(x + x_inc, y + y_inc):
                if board[x + x_inc][y + y_inc] != 0 and board[x + x_inc][y + y_inc] != current_colour:
                    #Check to see if there is a connected friendly piece in that direction
                    for step in range(2,8):
                        x_step = x + x_inc*step
                        y_step = y + y_inc*step
                        if self.withinBoardScope(x_step, y_step):
                            if board[x_step][y_step] == current_colour:
                                moveSupported = True
                                board[x][y] = current_colour
                                self.flipTiles(x, y, x_step, y_step, x_inc, y_inc, current_colour, board)
                                break
                            if board[x_step][y_step] == 0:
                                break
        return moveSupported

    # Helper function to flip all captured tiles in a move
    def flipTiles(self, x_start, y_start, x_end, y_end, direction_x, direction_y, current_colour, board):
        for step in range(1,8):
            x_step = x_start + direction_x*step
            y_step = y_start + direction_y*step
            if x_step == x_end and y_step == y_end:
                break
            else:
                board[x_step][y_step] = current_colour

    # Check to see if a perticular position is within the scope of the board
    def withinBoardScope(self, x, y):
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            return True
        return False

    # Create all the child nodes for a GameTreeNode
    def generateChildNodes(self):
        children_generated = False
        i = 0
        for row in self.nodeBoard:
            j = 0
            for cell in row:
                if cell == 0:
                    newBoardBlack = self.getBoardCopy()
                    newBoardWhite = self.getBoardCopy()
                    if self.checkMoveValidAndPerform('B',i,j,newBoardBlack):
                        children_generated = True
                        newBoardBlack[i][j] = 'B'
                        self.children_black.append(GameTreeNode(ReversiBoard('B[{}][{}]'.format(i,j), newBoardBlack), self))
                    if self.checkMoveValidAndPerform('W',i,j,newBoardWhite):
                        children_generated = True
                        newBoardWhite[i][j] = 'W'
                        self.children_white.append(GameTreeNode(ReversiBoard('W[{}][{}]'.format(i,j), newBoardWhite), self))
                j = j + 1
            i = i + 1

        self.isTerminal = not children_generated