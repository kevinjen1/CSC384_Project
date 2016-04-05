
def canMove(self,opp,array):
    if array[0] != opp: return False
    for i in range(8):
        if array[i] == 0: return False
        if array[i] == self: return True
    return False


def isLeagelMove(self,opp,game_board,x_start,y_start,board_size):
    if game_board[x_start][y_start] != 0: return False
    array = [0] * board_size
    dy = dx = -1
    while dy <= 1:
        while dx <= 1:
            if (not dy) and (not dx): continue
            for i in range(board_size):
                x = x_start + (i+1)*dx
                y = y_start + (i+1)*dy
                if 0 <= x < board_size and 0 <= y < board_size: array[i] = game_board[x][y]
                else: array[i] = None
            if canMove(self,opp,array): return True
            dx += 1
        dy += 1
    return False


def NumValidMoves(self,opp,game_board,board_size):
    count = 0
    for i in range(board_size):
        for j in range(board_size):
            if isLeagelMove(self, opp, game_board, i, j, board_size): count += 1
    return count


def Hfunc(game_board):
    board_size = len(game_board)
    my_color = 'W'
    opp_color = 'B'
    parity = stability_flip = stability_weight = corners = mobility = 0.00

    # indices to loop through 8 adjacent slot for a given slot
    x_iter = [-1, -1, 0, 1, 1, 1, 0, -1]
    y_iter = [0, 1, 1, 1, 0, -1, -1, -1]

    # educated guesses of the weight of each slot
    W = [[20, -3, 11, 8, 8, 11, -3, 20],
         [-3, -7, -4, 1, 1, -4, -7, -3],
         [11, -4, 2, 2, 2, 2, -4, 11],
         [8, 1, 2, -3, -3, 2, 1, 8],
         [8, 1, 2, -3, -3, 2, 1, 8],
         [11, -4, 2, 2, 2, 2, -4, 11],
         [-3, -7, -4, 1, 1, -4, -7, -3],
         [20, -3, 11, 8, 8, 11, -3, 20]]

    # difference in number of tiles

    # if one tile is adjacent to a empty slot and so can be potentially flipped
    my_tiles = opp_tiles = 0
    my_unstable_tiles = opp_unstable_tiles = 0
    for i in range(board_size):
        for j in range(board_size):
            if game_board[i][j] == my_color:
                stability_weight += W[i][j]
                my_tiles += 1
            elif game_board[i][j] == opp_color:
                stability_weight -= W[i][j]
                opp_tiles += 1
            if game_board[i][j] != 0:
                for k in range(8):
                    x = i + x_iter[k]
                    y = j + y_iter[k]
                    if 0<=x<board_size and 0<=y<board_size and not game_board[x][y]:
                        if game_board[i][j] == my_color: my_unstable_tiles += 1
                        else: opp_unstable_tiles += 1

    parity = 100 * (my_tiles - opp_tiles)/(my_tiles + opp_tiles)
    if my_unstable_tiles + opp_unstable_tiles == 0:
        stability_flip = 0
    else:
        stability_flip = -100 * (my_unstable_tiles - opp_unstable_tiles)/(my_unstable_tiles + opp_unstable_tiles)

    # four corners
    my_tiles = opp_tiles = 0
    if game_board[0][0] == my_color: my_tiles += 1
    elif game_board[0][0] == opp_color: opp_tiles += 1
    if game_board[0][board_size-1] == my_color: my_tiles += 1
    elif game_board[0][board_size-1] == opp_color: opp_tiles += 1
    if game_board[board_size-1][0] == my_color: my_tiles += 1
    elif game_board[board_size-1][0] == opp_color: opp_tiles += 1
    if game_board[board_size-1][board_size-1] == my_color: my_tiles += 1
    elif game_board[board_size-1][board_size-1] == opp_color: opp_tiles += 1
    if my_tiles + opp_tiles == 0:
        corners = 0
    else:
        corners = 100 * (my_tiles - opp_tiles)/(my_tiles + opp_tiles)

    # mobility
    my_tiles = NumValidMoves(my_color,opp_color,game_board,board_size)
    opp_tiles = NumValidMoves(opp_color,my_color,game_board,board_size)
    if my_tiles + opp_tiles == 0:
        mobility = 0
    else:
        mobility = 100 * (my_tiles - opp_tiles)/(my_tiles + opp_tiles)

    final_weight = 10 * parity + 74.396 * stability_flip + 10 * stability_weight + 801.724 * corners + 78.922 * mobility
    return final_weight















