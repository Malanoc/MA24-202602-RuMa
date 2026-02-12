# gfx.py

import pygame
import pygame.gfxdraw
import core

CELL_SIZE = 90
GREEN = (20, 110, 20)
BLACK_COLOR = (30, 30, 30)
WHITE_COLOR = (245, 245, 245)


def init_window():
    pygame.init()
    width = height = core.BOARD_SIZE * CELL_SIZE
    screen = pygame.display.set_mode((width, height + 50))
    pygame.display.set_caption("Othello")
    font = pygame.font.SysFont(None, 32)
    return screen, font


def draw_piece(surface, center, radius, color):
    x, y = center
    pygame.gfxdraw.filled_circle(surface, x, y, radius, color)
    pygame.gfxdraw.aacircle(surface, x, y, radius, color)


def draw_board(screen, board):
    screen.fill(GREEN)

    for x in range(core.BOARD_SIZE):
        for y in range(core.BOARD_SIZE):
            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

            if board[x][y] != core.EMPTY:
                color = BLACK_COLOR if board[x][y] == core.BLACK else WHITE_COLOR
                draw_piece(
                    screen,
                    rect.center,
                    CELL_SIZE // 2 - 10,
                    color
                )


def draw_ui(screen, font, player, board):
    black, white = core.score(board)
    text = f"Noir: {black}   Blanc: {white}   Tour: {'Noir' if player == core.BLACK else 'Blanc'}"
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, (10, core.BOARD_SIZE * CELL_SIZE + 10))
