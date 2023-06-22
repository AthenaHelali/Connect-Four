import random
import numpy as np
import pygame
import sys
import math

BACKGROUND = (204, 204, 255)
CIRCLE_COLOR = (153, 153, 255)
YELLOW = (255, 255, 102)
RED = (255, 0, 102)
RADIUS = 45

Row_Num = 6
Column_Num = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2
 
def create_board():
    board = np.zeros((Row_Num,Column_Num))
    return board

def drop_piece(board, row, column, piece):
    board[row][column] = piece

def is_valid_location(board, column ):
    return board[Row_Num-1][column] == 0
    

def get_next_open_row(board, column):
    for r in range(Row_Num):
        if board[r][column] == 0:
            return r
     
def print_board(board):
    print(np.flip(board,0))

def winning_move(board, piece, col, row):

    # check horizontal move
    for c in range(Column_Num-3):
        if board[row][c] == piece and board[row][c+1]==piece and board[row][c+2]==piece and board[row][c+3] == piece:
            return True

     # check vertical move   
    for r in range(Row_Num-3):
        if board[r][col] == piece and board[r+1][col]==piece and board[r+2][col]==piece and board[r+3][col] == piece:
            return True
        
    #check positively sloped diaganols
    for c in range(Column_Num-3):
        for r in range(Row_Num-3):
            if board[r][c]== piece and board[r+1][c+1]== piece and board[r+2][c+2]== piece and board[r+3][c+3]== piece:
                return True

    #check negatively sloped diaganols

    for c in range(3, Column_Num):
        for r in range(3, Row_Num):
            if board[r][c]== piece and board[r-1][c+1]== piece and board[r-2][c+2]== piece and board[r-3][c+3]== piece:
                return True
            
def score_position(board, piece):
    #score horizontal
    score = 0
    for r in range(Row_Num):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(Column_Num-3):
            window = row_array[c:c+4]
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 10
    return score

def get_valid_locations(board):
    valid_locations = []
    for col in range(Column_Num):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board,piece):
    valid_locations = get_valid_locations(board)


def draw_board(board):
    for c in range(Column_Num):
        for r in range(Row_Num):
            pygame.draw.rect(screen, BACKGROUND, (c*100, r*100+100, 100, 100))
            pygame.draw.circle(screen, CIRCLE_COLOR,(c*100+55, r*100+150),RADIUS)
           
    
    for c in range(Column_Num):
        for r in range(Row_Num):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED,(c*100+55, 700 - (r*100+50)),RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW,(c*100+55, 700 - (r*100+50)),RADIUS)

    pygame.display.update()



 
board = create_board()
game_over = False

pygame.init()
size = (700,700)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

Font = pygame.font.SysFont("monospace", 75)
turn = random.randint(PLAYER,AI)


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BACKGROUND, (0,0, 700,100))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED,(posx, 50),RADIUS)
            
            pygame.display.update()




        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BACKGROUND, (0,0, 700,100))
            #Player 1 input
            if turn == PLAYER:
                posx = event.pos[0]
                column = int(math.floor(posx/100))

                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE, column, row ):
                        label = Font.render ("player1 wins",1 ,RED)
                        screen.blit(label,(60,10))
                        game_over = True
                    turn +=1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)





            #Player2 input
        if turn == AI and not game_over:
            column = random.randint(0, Column_Num-1)

            if is_valid_location(board, column):
                pygame.time.wait(500)
                row = get_next_open_row(board, column)
                drop_piece(board, row, column, AI_PIECE)

                if winning_move(board, AI_PIECE, column, row ):
                    label = Font.render ("player2 wins",1 ,RED)
                    screen.blit(label,(60 ,10))
                    game_over = True

            print_board(board)
            draw_board(board)
            turn +=1
            turn = turn % 2
        if game_over:
            pygame.time.wait(5000)
