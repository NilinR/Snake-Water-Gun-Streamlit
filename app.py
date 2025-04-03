import streamlit as s
import numpy as np

s.set_page_config(page_title="Snake Water Gun", page_icon=":snake:",layout="wide")

# Define the actions (Snake, Water, Gun)
actions = {0: "Snake", 1: "Water", 2: "Gun"}

# Define the Q-learning parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.5  # Exploration rate (increased for more exploration)

# Initialize the Q-table
q_table = np.zeros((len(actions), len(actions)))

# Function to select action based on epsilon-greedy policy
def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(len(actions))
    else:
        return np.argmax(q_table[state, :])

# Function to update Q-values using Q-learning
def update_q_table(state, action, reward, next_state):
    q_predict = q_table[state, action]
    q_target = reward + gamma * np.max(q_table[next_state, :])
    q_table[state, action] += alpha * (q_target - q_predict)

# Function to simulate a single game episode
def play_game(k):
    # Initial state
    state = np.random.choice(len(actions))
    
    # Print scoreboard
    s.write("Scoreboard: You - {}, Computer - {}".format(score[0], score[1]))
    
    # Ask for player's action
    player_action =s.number_input("Your action (0: Snake, 1: Water, 2: Gun): ",max_value=2,key=k,value=None, step=1)
    
    # Convert player's action to index
    if(isinstance(player_action, int)):
        player_index = player_action
        # Computer's action
        computer_action_index = choose_action(state)
        computer_action = actions[computer_action_index]
    
        # Determine the reward
        reward = 0
        if (player_index == 0 and computer_action_index == 1) or \
           (player_index == 1 and computer_action_index == 2) or \
           (player_index == 2 and computer_action_index == 0):
            reward = 1
        elif (player_index == 0 and computer_action_index == 2) or \
             (player_index == 1 and computer_action_index == 0) or \
             (player_index == 2 and computer_action_index == 1):
            reward = -1
    
        # Update Q-values
        update_q_table(state, player_index, reward, computer_action_index)
    
        # Update scoreboard
        if reward == 1:
            score[0] += 1
        elif reward == -1:
            score[1] += 1
    
        # Print choices and result
        s.write("Your choice: {}, Computer's choice: {}".format(actions[player_action], computer_action))
        if reward == 1:
            s.write("You win!")
            return True
        elif reward == -1:
            s.write("Computer wins!")
            return False
        else:
            s.write("It's a tie!")
            return None
        
# Main function
if __name__ == "__main__":
    s.title("Welcome to Snake Water Gun game!")
    # Ask for number of rounds to play

    num_rounds =s.number_input("How many rounds do you want to play? ",min_value=1, step=1)
        
    # Initialize scoreboard
    score = [0, 0]  # [Your score, Computer's score]
        
     # Play the game for specified rounds
    for rounds in range(num_rounds):
            s.write("")
            s.write("Round",rounds+1)
            result = play_game(rounds)
            if result is True:
                s.write("Congratulations! You won this round.")
            elif result is False:
                s.write("You lost this round. Try again!")
            s.write("")

    s.write("")
    s.write("\nFinal Scoreboard: You - {}, Computer - {}".format(score[0], score[1]))

        
        

