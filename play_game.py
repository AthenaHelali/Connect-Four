import numpy as np
import CF
from tensorflow.keras.models import load_model
model = load_model('connect_four_dqn_final.h5')
game = CF.ConnectFour()
def get_best_move(state):
    q_values = model.predict(state.reshape(1, -1))[0]
    valid_moves = game.get_valid_moves()
    best_move = valid_moves[np.argmax(q_values[valid_moves])]
    return best_move

while not game.is_game_over():
    game.print_board()
    
    if game.current_player == 1:
        # Player's turn
        column = int(input("Enter your move (column number): "))


    else:
        # Agent's turn
        state = game.get_state()
        column = get_best_move(state)
    game.current_player = (game.current_player % 2) + 1

    game.make_move(column)

# Print the final board state
game.print_board()


