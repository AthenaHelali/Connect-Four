import random
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


class ConnectFour:
    def __init__(self):
        self.row_num = 6
        self.column_num = 7
        self.player_piece = 1
        self.current_player = random.randint(1,2)
        self.ai_piece = 2
        self.board = [[0] * self.column_num for _ in range(self.row_num)]

    def get_state(self):
        return self.board.flatten()

    def make_move(self,column, piece):
        row = self.get_next_open_row(column)
        self.board[row][column] = piece
        

    def is_valid_move(self, column):
        return self.board[self.row_num - 1][column] == 0

    def get_next_open_row(self, column):
        for r in range(self.row_num):
            if self.board[r][column] == 0:
                return r
    
    def print_board(self):
        print(np.flip(self.board,0))

    def winning_move(self, piece):
        # Check horizontal moves
        for r in range(self.row_num):
            for c in range(self.column_num - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r][c + 1] == piece
                    and self.board[r][c + 2] == piece
                    and self.board[r][c + 3] == piece
                ):
                    return True

        # Check vertical moves
        for r in range(self.row_num - 3):
            for c in range(self.column_num):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c] == piece
                    and self.board[r + 2][c] == piece
                    and self.board[r + 3][c] == piece
                ):
                    return True

        # Check positively sloped diagonals
        for r in range(self.row_num - 3):
            for c in range(self.column_num - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c + 1] == piece
                    and self.board[r + 2][c + 2] == piece
                    and self.board[r + 3][c + 3] == piece
                ):
                    return True

        # Check negatively sloped diagonals
        for r in range(3, self.row_num):
            for c in range(self.column_num - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r - 1][c + 1] == piece
                    and self.board[r - 2][c + 2] == piece
                    and self.board[r - 3][c + 3] == piece
                ):
                    return True

        return False

    def evaluate_window(self, window, piece):
        score = 0
        opponent_piece = self.player_piece if piece == self.ai_piece else self.ai_piece

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def score_position(self, piece):
        score = 0

        # Score center column
        center_column = [self.board[r][self.column_num // 2] for r in range(self.row_num)]
        score += center_column.count(piece) * 3

        # Score horizontal
        for r in range(self.row_num):
            row = self.board[r]
            for c in range(self.column_num - 3):
                window = row[c : c + 4]
                score += self.evaluate_window(window, piece)

        # Score vertical
        for c in range(self.column_num):
            column = [self.board[r][c] for r in range(self.row_num)]
            for r in range(self.row_num - 3):
                window = column[r : r + 4]
                score += self.evaluate_window(window, piece)

        # Score positive sloped diagonal
        for r in range(self.row_num - 3):
            for c in range(self.column_num - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        # Score negative sloped diagonal
        for r in range(self.row_num - 3):
            for c in range(self.column_num - 3):
                window = [self.board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score
    
    

    def is_terminal_node(self):
        return self.winning_move(self.player_piece) or self.winning_move(self.ai_piece) or len(
            self.get_valid_moves()
        ) == 0

    def get_valid_moves(self):
        valid_locations = []
        for c in range(self.column_num):
            if self.is_valid_move(c):
                valid_locations.append(c)
        return valid_locations

    def minimax(self, depth, alpha, beta, maximizing_player):
        valid_locations = self.get_valid_moves()
        is_terminal = self.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(self.ai_piece):
                    return (None, 100000000000000)
                elif self.winning_move(self.player_piece):
                    return (None, -10000000000000)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(self.ai_piece))
        if maximizing_player:
            value = -float("inf")
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(col)
                b_copy = [row[:] for row in self.board]
                self.make_move( col, self.ai_piece)
                new_score = self.minimax(depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
                self.board = [row[:] for row in b_copy]
            return column, value
        else:
            value = float("inf")
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(col)
                b_copy = [row[:] for row in self.board]
                self.make_move(col, self.player_piece)
                new_score = self.minimax(depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
                self.board = [row[:] for row in b_copy]
            return column, value
    
    def draw_board(self):
        size = (700,700)
        screen = pygame.display.set_mode(size)
        for c in range(self.column_num):
            for r in range(self.row_num):
                pygame.draw.rect(screen, BACKGROUND, (c*100, r*100+100, 100, 100))
                pygame.draw.circle(screen, CIRCLE_COLOR,(c*100+55, r*100+150),RADIUS)

        for c in range(self.column_num):
            for r in range(self.row_num):
                if self.board[r][c] == self.player_piece:
                    pygame.draw.circle(screen, RED,(c*100+55, 700 - (r*100+50)),RADIUS)
                elif self.board[r][c] == self.ai_piece:
                    pygame.draw.circle(screen, YELLOW,(c*100+55, 700 - (r*100+50)),RADIUS)

        pygame.display.update()
            

    def play(self):
        game_over = False

        pygame.init()
        size = (700,700)
        screen = pygame.display.set_mode(size)
        self.draw_board()
        pygame.display.update()

        Font = pygame.font.SysFont("monospace", 75)


        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BACKGROUND, (0,0, 700,100))
                    posx = event.pos[0]
                    if self.current_player == 1:
                        pygame.draw.circle(screen, RED,(posx, 50),RADIUS/2)
                    
                    pygame.display.update()




                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BACKGROUND, (0,0, 700,100))
                    #Player 1 input
                    if self.current_player == 1 :
                        posx = event.pos[0]
                        column = int(math.floor(posx/100))

                        if self.is_valid_move(column):
                            self.make_move(column, self.player_piece)
                            if self.winning_move(self.player_piece):
                                label = Font.render ("player1 wins",1 ,RED)
                                screen.blit(label,(60,10))
                                game_over = True
                            self.print_board()
                            self.draw_board()
                            self.current_player %= 2
                            self.current_player +=1





                    #Player2 input
                if self.current_player == 2 and not game_over:
                    column, minimax_score  = self.minimax(6, -math.inf, math.inf, True)
                    if self.is_valid_move(column):
                        self.make_move(column, self.ai_piece)

                        if self.winning_move(self.ai_piece):
                            label = Font.render ("player2 wins",1 ,RED)
                            screen.blit(label,(60 ,10))
                            game_over = True

                    self.print_board()
                    self.draw_board()
                    self.current_player %= 2
                    self.current_player +=1
                    
                if game_over:
                    pygame.time.wait(5000)

if __name__ == "__main__":
    game = ConnectFour()
    game.play()