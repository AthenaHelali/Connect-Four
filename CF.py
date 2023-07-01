import numpy as np
import random
class ConnectFour:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows, columns))
        self.current_player = 1
        self.game_over = False

    def reset(self):
        self.board = np.zeros((self.rows, self.columns))
        self.current_player = 1
        self.game_over = False

    def is_valid_move(self, column):
        return self.board[0][column] == 0

    def make_move(self, column):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                break

    def evaluate_state(self):
        # Define the evaluation weights for different features
        weights = [3, 4, 5, 7, 5, 4, 3]
        score = 0

        # Evaluate rows
        for row in range(self.rows):
            for col in range(self.columns - 3):
                window = self.board[row, col:col + 4]
                score += self.evaluate_window(window)

        # Evaluate columns
        for col in range(self.columns):
            for row in range(self.rows - 3):
                window = self.board[row:row + 4, col]
                score += self.evaluate_window(window)

               # Evaluate positively sloped diagonals
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                window = self.board[row:row + 4, col:col + 4].diagonal()
                score += self.evaluate_window(window)

        # Evaluate negatively sloped diagonals
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                window = np.fliplr(self.board[row - 3:row + 1, col:col + 4]).diagonal()
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):
        score = 0

        # Evaluate the window based on the player's pieces and weights
        if np.count_nonzero(window == self.current_player) == 4:
            score += 100
        elif np.count_nonzero(window == self.current_player) == 3 and np.count_nonzero(window == 0) == 1:
            score += 5
        elif np.count_nonzero(window == self.current_player) == 2 and np.count_nonzero(window == 0) == 2:
            score += 2

        opponent = 1 if self.current_player == 2 else 2
        if np.count_nonzero(window == opponent) == 3 and np.count_nonzero(window == 0) == 1:
            score -= 4

        return score
    

    def minimax(self, depth, alpha, beta, maximizing_player):
        valid_moves = self.get_valid_moves()

        if depth == 0 or self.is_game_over():
            if maximizing_player:
                return None, self.evaluate_state()
            else:
                return None, -self.evaluate_state()

        best_move = random.choice(valid_moves)  # Randomly choose a move initially
        if maximizing_player:
            max_eval = -float('inf')
            for move in valid_moves:
                self.make_move(move)
                _, eval = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break
            return best_move, max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                self.make_move(move)
                _, eval = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if alpha >= beta:
                    break
            return best_move, min_eval

        
    def undo_move(self, column):
        for row in range(self.rows):
            if self.board[row][column] != 0:
                self.board[row][column] = 0
                break




    def check_winner(self):
        # Check rows
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if (
                    self.board[row][col]
                    and self.board[row][col] == self.board[row][col + 1]
                    == self.board[row][col + 2]
                    == self.board[row][col + 3]
                ):
                    return self.board[row][col]

        # Check columns
        for row in range(self.rows - 3):
            for col in range(self.columns):
                if (
                    self.board[row][col]
                    and self.board[row][col] == self.board[row + 1][col]
                    == self.board[row + 2][col]
                    == self.board[row + 3][col]
                ):
                    return self.board[row][col]

        # Check diagonals (top-left to bottom-right)
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if (
                    self.board[row][col]
                    and self.board[row][col] == self.board[row + 1][col + 1]
                    == self.board[row + 2][col + 2]
                    == self.board[row + 3][col + 3]
                ):
                    return self.board[row][col]

        # Check diagonals (bottom-left to top-right)
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if (
                    self.board[row][col]
                    and self.board[row][col] == self.board[row - 1][col + 1]
                    == self.board[row - 2][col + 2]
                    == self.board[row - 3][col + 3]
                ):
                    return self.board[row][col]

        # Check for a draw
        if np.all(self.board):
            return 0

        return None
  

    def is_game_over(self):
        # Check for horizontal win
        for row in range(6):
            for col in range(4):
                if self.board[row, col] == self.board[row, col+1] == self.board[row, col+2] == self.board[row, col+3] != 0:
                    return True

        # Check for vertical win
        for col in range(7):
            for row in range(3):
                if self.board[row, col] == self.board[row+1, col] == self.board[row+2, col] == self.board[row+3, col] != 0:
                    return True

        # Check for diagonal win (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if self.board[row, col] == self.board[row+1, col+1] == self.board[row+2, col+2] == self.board[row+3, col+3] != 0:
                    return True

        # Check for diagonal win (top-right to bottom-left)
        for row in range(3):
            for col in range(3, 7):
                if self.board[row, col] == self.board[row+1, col-1] == self.board[row+2, col-2] == self.board[row+3, col-3] != 0:
                    return True

        # Check for a draw
        if np.all(self.board):
            return True

        return False
    
    def winning_move(self, piece):
    # Check horizontal moves
        for r in range(self.rows):
            for c in range(self.columns - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r][c + 1] == piece
                    and self.board[r][c + 2] == piece
                    and self.board[r][c + 3] == piece
                ):
                    return True

        # Check vertical moves
        for r in range(self.rows - 3):
            for c in range(self.columns):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c] == piece
                    and self.board[r + 2][c] == piece
                    and self.board[r + 3][c] == piece
                ):
                    return True

        # Check positively sloped diagonals
        for r in range(self.rows - 3):
            for c in range(self.columns - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c + 1] == piece
                    and self.board[r + 2][c + 2] == piece
                    and self.board[r + 3][c + 3] == piece
                ):
                    return True

        # Check negatively sloped diagonals
        for r in range(3, self.rows):
            for c in range(self.columns - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r - 1][c + 1] == piece
                    and self.board[r - 2][c + 2] == piece
                    and self.board[r - 3][c + 3] == piece
                ):
                    return True

        return False


    def get_state(self):
        return self.board.flatten()

    def get_valid_moves(self):
        return [col for col in range(self.columns) if self.is_valid_move(col)]

    def print_board(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] == 0:
                    print(".", end=" ")
                elif self.board[row][col] == 1:
                    print("X", end=" ")
                else:
                    print("O", end=" ")
            print()

            

def main():
    game = ConnectFour()

    while True:
        game.print_board()
        print(game.current_player)

        if game.current_player == 1:
            column = int(input("Player 1, make your move (0-6): "))
        else:
            column, _ = game.minimax(4, -float("inf"), float("inf"), True)
            print("AI's move:", column)

        if game.is_valid_move(column):
            game.make_move(column)

            if game.check_winner() is not None:
                if game.check_winner() == 1:
                    print("Player 1 wins!")
                else:
                    print("AI wins!")
                break
            elif game.is_game_over():
                print("It's a tie!")
                break

            game.current_player = (game.current_player % 2) + 1
        else:
            print("Invalid move. Please try again.")

    game.print_board()

if __name__ == "__main__":
    main()


