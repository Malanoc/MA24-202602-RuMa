# core.py

BOARD_SIZE = 8

EMPTY = 0
BLACK = 1
WHITE = -1

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


def create_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    board[3][3] = WHITE
    board[4][4] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK

    return board


def on_board(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


def flips(board, x, y, player):
    pieces = []

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        temp = []

        while on_board(nx, ny) and board[nx][ny] == -player:
            temp.append((nx, ny))
            nx += dx
            ny += dy

        if on_board(nx, ny) and board[nx][ny] == player and temp:
            pieces.extend(temp)

    return pieces


def valid_moves(board, player):
    moves = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == EMPTY and flips(board, x, y, player):
                moves.append((x, y))
    return moves


def apply_move(board, x, y, player):
    to_flip = flips(board, x, y, player)

    if not to_flip:
        return False

    board[x][y] = player
    for fx, fy in to_flip:
        board[fx][fy] = player

    return True


def score(board):
    black = sum(row.count(BLACK) for row in board)
    white = sum(row.count(WHITE) for row in board)
    return black, white
