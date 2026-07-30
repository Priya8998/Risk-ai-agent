import csv
import io
import os

from contextlib import redirect_stdout
from risk_game import play_game


# ==================================================
# Choose the agents
# ==================================================

agent_a = "Monte Carlo Agent"
agent_b = "Heuristic Agent"


# ==================================================
# Experiment settings
# ==================================================

number_of_games = 20
maximum_turns = 100


# ==================================================
# Create results folder and filename
# ==================================================

os.makedirs("results", exist_ok=True)

safe_agent_a = agent_a.replace(" ", "_").lower()
safe_agent_b = agent_b.replace(" ", "_").lower()

csv_file = (
    f"results/{safe_agent_a}_vs_{safe_agent_b}.csv"
)


# ==================================================
# Experiment counters
# ==================================================

agent_a_wins = 0
agent_b_wins = 0
draws = 0
total_turns = 0


print("\nRunning experiments...")
print("----------------------")
print("Agent A:", agent_a)
print("Agent B:", agent_b)
print("Games:", number_of_games)


# ==================================================
# Create the CSV file
# ==================================================

with open(
    csv_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "game_number",
        "player_1_agent",
        "player_2_agent",
        "winner_player",
        "winning_agent",
        "turns_played",

        "player_1_attacks",
        "player_1_successful_attacks",
        "player_1_armies_lost",
        "player_1_territories_captured",
        "player_1_decisions",
        "player_1_decision_time",
        "player_1_simulations",

        "player_2_attacks",
        "player_2_successful_attacks",
        "player_2_armies_lost",
        "player_2_territories_captured",
        "player_2_decisions",
        "player_2_decision_time",
        "player_2_simulations"
    ])


    # ==================================================
    # Run all games
    # ==================================================

    for game_number in range(
        1,
        number_of_games + 1
    ):

        # Alternate starting positions
        if game_number % 2 == 1:

            player_1_agent = agent_a
            player_2_agent = agent_b

        else:

            player_1_agent = agent_b
            player_2_agent = agent_a


        # Hide detailed game output
        hidden_output = io.StringIO()

        with redirect_stdout(hidden_output):

            winner, turns_played, metrics = play_game(
                max_turns=maximum_turns,
                player_1_agent=player_1_agent,
                player_2_agent=player_2_agent
            )


        # Find the winning agent
        if winner == "Player 1":

            winning_agent = player_1_agent

        elif winner == "Player 2":

            winning_agent = player_2_agent

        else:

            winning_agent = "Draw"


        # Count wins and draws
        if winning_agent == agent_a:

            agent_a_wins += 1

        elif winning_agent == agent_b:

            agent_b_wins += 1

        else:

            draws += 1


        total_turns += turns_played


        # ==================================================
        # Read Player 1 metrics
        # ==================================================

        player_1_metrics = metrics["Player 1"]

        player_1_attacks = (
            player_1_metrics["attacks_made"]
        )

        player_1_successful_attacks = (
            player_1_metrics["successful_attacks"]
        )

        player_1_armies_lost = (
            player_1_metrics["armies_lost"]
        )

        player_1_territories_captured = (
            player_1_metrics["territories_captured"]
        )

        player_1_decisions = (
            player_1_metrics["decisions_made"]
        )

        player_1_decision_time = (
            player_1_metrics["decision_time_seconds"]
        )

        player_1_simulations = (
            player_1_metrics["simulations_run"]
        )


        # ==================================================
        # Read Player 2 metrics
        # ==================================================

        player_2_metrics = metrics["Player 2"]

        player_2_attacks = (
            player_2_metrics["attacks_made"]
        )

        player_2_successful_attacks = (
            player_2_metrics["successful_attacks"]
        )

        player_2_armies_lost = (
            player_2_metrics["armies_lost"]
        )

        player_2_territories_captured = (
            player_2_metrics["territories_captured"]
        )

        player_2_decisions = (
            player_2_metrics["decisions_made"]
        )

        player_2_decision_time = (
            player_2_metrics["decision_time_seconds"]
        )

        player_2_simulations = (
            player_2_metrics["simulations_run"]
        )


        # ==================================================
        # Save the game result
        # ==================================================

        writer.writerow([
            game_number,
            player_1_agent,
            player_2_agent,
            winner,
            winning_agent,
            turns_played,

            player_1_attacks,
            player_1_successful_attacks,
            player_1_armies_lost,
            player_1_territories_captured,
            player_1_decisions,
            player_1_decision_time,
            player_1_simulations,

            player_2_attacks,
            player_2_successful_attacks,
            player_2_armies_lost,
            player_2_territories_captured,
            player_2_decisions,
            player_2_decision_time,
            player_2_simulations
        ])


        print(
            "Game",
            game_number,
            "completed - Winner:",
            winning_agent
        )


# ==================================================
# Calculate summary results
# ==================================================

agent_a_win_rate = (
    agent_a_wins / number_of_games
) * 100

agent_b_win_rate = (
    agent_b_wins / number_of_games
) * 100

draw_rate = (
    draws / number_of_games
) * 100

average_turns = (
    total_turns / number_of_games
)


# ==================================================
# Display summary
# ==================================================

print("\n================================")
print("Experiment Results")
print("================================")

print("Games played:", number_of_games)

print("\nAgent A:", agent_a)
print("Wins:", agent_a_wins)
print(
    "Win rate:",
    round(agent_a_win_rate, 2),
    "%"
)

print("\nAgent B:", agent_b)
print("Wins:", agent_b_wins)
print(
    "Win rate:",
    round(agent_b_win_rate, 2),
    "%"
)

print("\nDraws:", draws)
print(
    "Draw rate:",
    round(draw_rate, 2),
    "%"
)

print(
    "\nAverage turns:",
    round(average_turns, 2)
)

print(
    "\nResults saved to:",
    csv_file
)