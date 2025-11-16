"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


class board:
    def __init__(self, state=None):
        """
        state: 可选的创建已有的board的新的类
        board的实例对象与列表一致，因此不影响runner中列表的使用
        """
        import copy

        if isinstance(state, board):
            self._board = copy.deepcopy(state._board)
        elif state is None:
            # 初始化创建新列表类
            self._board = [
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
            ]
        else:
            # 若传入3x3列表
            self._board = copy.deepcopy(state)

        # 维护x,o的数量，提高检索效率
        self.x = 0
        self.o = 0
        for row in self._board:
            for cell in row:
                if cell == X:
                    self.x += 1
                elif cell == O:
                    self.o += 1

    def isEmpty(self):
        """如果棋盘所有格子均为 EMPTY(None)，返回 True。"""
        return self.x == 0 and self.o == 0

    def isFull(self):
        return self.x + self.o == 9

    # 让board支持列表的行为
    def __getitem__(self, idx):
        return self._board[idx]

    def __iter__(self):
        return iter(self._board)

    def __len__(self):
        return len(self._board)

    def copy(self):
        """返回 board 的深拷贝（新的 board 实例）。"""
        return board(self._board)

    def as_list(self):
        """返回内部状态的独立列表副本（用于需要真实列表的地方）。"""
        import copy

        return copy.deepcopy(self._board)

    def place(self, action, player):
        """
        action: [i,j]列表，表示在i,j位置放入player元素
        player: X或O，表示玩家
        """
        i, j = action
        if self._board[i][j] is not EMPTY:
            return False  # 违法的添加，应该重新选择
        self._board[i][j] = player
        if player == X:
            self.x += 1
        else:
            self.o += 1
        return True  # 添加成功


def initial_state():
    """
    Returns starting state of the board.
    """
    return board()


def player(board):
    """
        Returns player who has the next turn on a board.
        The player function should take a board state as input, and return which player’s turn it is (either X or O).
    In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
    Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    """
    if board.isEmpty() or board.isFull():
        return X
    if board.x > board.o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    ret = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                ret.add((i, j))
    return ret


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newboard = board.copy()
    curplayer = player(board)
    newboard.place(action, curplayer)
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    b = getattr(board, "_board", board)

    # 检查每一行
    for i in range(3):
        if b[i][0] is not None and b[i][0] == b[i][1] == b[i][2]:
            return b[i][0]

    # 检查每一列
    for j in range(3):
        if b[0][j] is not None and b[0][j] == b[1][j] == b[2][j]:
            return b[0][j]

    # 检查两条对角线
    if b[0][0] is not None and b[0][0] == b[1][1] == b[2][2]:
        return b[0][0]
    if b[0][2] is not None and b[0][2] == b[1][1] == b[2][0]:
        return b[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) or board.isFull()


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def maxValue(bd):
        if terminal(bd):
            return utility(bd), None
        v = -math.inf
        best_action = None
        for action in actions(bd):
            val, _ = minValue(result(bd, action))
            if val > v:
                v = val
                best_action = action
                if v == 1:  # 已达到最优，剪枝
                    break
        return v, best_action

    def minValue(bd):
        if terminal(bd):
            return utility(bd), None
        v = math.inf
        best_action = None
        for action in actions(bd):
            val, _ = maxValue(result(bd, action))
            if val < v:
                v = val
                best_action = action
                if v == -1:  # 已达到最优，剪枝
                    break
        return v, best_action

    return maxValue(board)[1] if player(board) == X else minValue(board)[1]
