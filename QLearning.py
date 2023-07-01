import numpy as np
import random
import CF
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam


# Connect Four game environment


# Deep Q-Learning agent
class DQNAgent:
    def __init__(self, state_size, action_size, exploration_rate=1.0, exploration_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95  # Discount factor
        self.epsilon = exploration_rate  # Exploration rate
        self.epsilon_decay = exploration_decay
        self.epsilon_min = 0.01
        self.learning_rate = 0.001


        # Q-Network
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(64, input_dim=self.state_size, activation="relu"))
        model.add(Dense(64, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(np.array([state]))
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                target = (
                    reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
                )
            target_f = self.model.predict(np.array([state]))
            target_f[0][action] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay



if __name__ == "__main__":
    # Initialize Connect Four game environment
    env = CF.ConnectFour()

    # Define the state and action sizes
    state_size = env.rows * env.columns
    action_size = env.columns

    # Initialize the DQN agent
    agent = DQNAgent(state_size, action_size)

    # Train the DQN agent
    episodes = 300
    batch_size = 32

    for episode in range(episodes):
        state = env.get_state()
        done = False

        while not done:
            reward = 0
            action = agent.act(state)
            if env.is_valid_move(action):
                env.make_move(action)
                next_state = env.get_state()
                winner = env.check_winner()

                if winner is not None:
                    reward = 1 if winner == 1 else -1
                    done = True
                elif winner == 0:
                    reward = 0
                    done = True

                agent.remember(state, action, reward, next_state, done)
                state = next_state

            # Termination condition: break out of the loop if the game is over
            if env.is_game_over():
                done = True
                if done:
                    print(
                        f"Episode: {episode + 1}/{episodes}, "
                        f"Score: {'Player 1 wins' if reward == 1 else 'Player 2 wins' if reward == -1 else 'Draw'}"
                    )
                    env.print_board()
                    break

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

        if episode % 100 == 0:
            agent.model.save("connect_four_dqn.h5")

        if episode == episodes - 1:
            agent.model.save("connect_four_dqn_final.h5")
            print("Training completed. Saved the final model.")
