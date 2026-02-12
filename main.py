# main.py

import pygame
import sys
import core
import gfx


def main():
    screen, font = gfx.init_window()
    clock = pygame.time.Clock()

    board = core.create_board()
    player = core.BLACK

    while True:
        clock.tick(60)

        moves = core.valid_moves(board, player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and moves:
                mx, my = pygame.mouse.get_pos()
                x = mx // gfx.CELL_SIZE
                y = my // gfx.CELL_SIZE

                if (x, y) in moves:
                    core.apply_move(board, x, y, player)
                    player *= -1

        if not moves:
            player *= -1
            if not core.valid_moves(board, player):
                pygame.quit()
                sys.exit()

        gfx.draw_board(screen, board)
        gfx.draw_ui(screen, font, player, board)
        pygame.display.flip()


if __name__ == "__main__":
    main()
