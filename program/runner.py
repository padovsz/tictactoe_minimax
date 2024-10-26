import pygame
import sys
import tictactoe
import time

pygame.init()

# constants
size = width, height = 600, 400
black = (0, 0, 0)
white = (255, 255, 255)
tile_size = 80
font_medium = pygame.font.Font('OpenSans-Regular.ttf', 28)
font_large = pygame.font.Font('OpenSans-Regular.ttf', 40)
font_move = pygame.font.Font('OpenSans-Regular.ttf', 60)
user = None
board = tictactoe.initial_state()
ai_turn = False

# set up display
screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    if user is None:
        # draw title
        title = font_large.render('Tic-Tac-Toe', True, white)
        title_rect = title.get_rect()
        title_rect.center = ((width / 2), 50)
        screen.blit(title, title_rect)

        # draw buttons
        play_x_button = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        play_x_text = font_medium.render('Play as X', True, black)
        play_x_rect = play_x_text.get_rect()
        play_x_rect.center = play_x_button.center
        pygame.draw.rect(screen, white, play_x_button)
        screen.blit(play_x_text, play_x_rect)

        play_o_button = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        play_o_text = font_medium.render('Play as O', True, black)
        play_o_rect = play_o_text.get_rect()
        play_o_rect.center = play_o_button.center
        pygame.draw.rect(screen, white, play_o_button)
        screen.blit(play_o_text, play_o_rect)

        # check if button is clicked
        if pygame.mouse.get_pressed()[0]:
            mouse = pygame.mouse.get_pos()
            if play_x_button.collidepoint(mouse):
                time.sleep(0.20)
                user = tictactoe.X
            else:
                if play_o_button.collidepoint(mouse):
                    time.sleep(0.20)
                    user = tictactoe.O
    else:
        # draw game board
        tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
        tiles = []

        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(tile_origin[0] + j * tile_size, tile_origin[1] + i * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != tictactoe.EMPTY:
                    move_text = font_move.render(board[i][j], True, white)
                    move_rect = move_text.get_rect()
                    move_rect.center = rect.center
                    screen.blit(move_text, move_rect)
                row.append(rect)
            tiles.append(row)

        game_over = tictactoe.terminal(board)
        player = tictactoe.player(board)

        # show title
        if game_over:
            winner = tictactoe.winner(board)
            if winner is None:
                title = f'Game Over: Tie.'
            else:
                title = f'Game Over: {winner} wins.'
        else:
            if user == player:
                title = f'Play as {user}.'
            else:
                title = f'Computing thinking . . .'

        title = font_large.render(title, True, white)
        title_rect = title.get_rect()
        title_rect.center = ((width / 2), 30)
        screen.blit(title, title_rect)

        # check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.50)
                move = tictactoe.minimax(board)
                board = tictactoe.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # check for a user move
        if pygame.mouse.get_pressed()[0] and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if board[i][j] == tictactoe.EMPTY and tiles[i][j].collidepoint(mouse):
                        board = tictactoe.result(board, (i, j))

        if game_over:
            again_button = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again_text = font_medium.render('Play Again', True, black)
            again_rect = again_text.get_rect()
            again_rect.center = again_button.center
            pygame.draw.rect(screen, white, again_button)
            screen.blit(again_text, again_rect)
            
            if pygame.mouse.get_pressed()[0]:
                mouse = pygame.mouse.get_pos()
                if again_button.collidepoint(mouse):
                    time.sleep(0.20)
                    user = None
                    board = tictactoe.initial_state()
                    ai_turn = False

    pygame.display.flip()
