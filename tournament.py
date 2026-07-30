import csv
import io
import os

from contextlib import redirect_stdout
from itertools import combinations

from risk_game import play_game


# ==================================================
# Tournament settings
# ==================================================

agents = [
    "Random Agent",
    "Rule-Based Agent",
    "Heuristic Agent",
    "Monte Carlo Agent"
]

# Use 20 while testing
games_per_pair = 20

# Maximum game length
maximum_turns = 100


# ==================================================
# Create results folder
# ==================================================

os.makedirs("results", exist_ok=True)

csv_file = "results/all_agents_tournament.csv"


# ==================================================
# Overall result records
# ==================================================

overall_results = {}

for agent_name in agents:

    overall_results[agent_name] = {
        "games": 0,
        "wins": 0,
        "draws": 0,
        "total_turns": 0,
        "attacks": 0,
        "successful_attacks": 0,
        "armies_lost": 0,
        "territories_captured": 0,
        "decisions": 0,
        "decision_time": 0.0,
        "simulations": 0
    }


# ==================================================
# Helper function to add metrics
# ==================================================

def add_agent_metrics(
    agent_name,
    player_metrics,
    turns_played
):

    results = overall_results[agent_name]

    results["games"] += 1
    results["total_turns"] += turns_played

    results["attacks"] += (
        player_metrics["attacks_made"]
    )

    results["successful_attacks"] += (
        player_metrics["successful_attacks"]
    )

    results["armies_lost"] += (
        player_metrics["armies_lost"]
    )

    results["territories_captured"] += (
        player_metrics["territories_captured"]
    )

    results["decisions"] += (
        player_metrics["decisions_made"]
    )

    results["decision_time"] += (
        player_metrics["decision_time_seconds"]
    )

    results["simulations"] += (
        player_metrics["simulations_run"]
    )


# ==================================================
# Start tournament
# ==================================================

print("\n================================")
print("All Agents Tournament")
print("================================")

print("Agents:", agents)
print("Games per pair:", games_per_pair)


with open(
    csv_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "match_number",
        "game_number",
        "agent_a",
        "agent_b",
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


    match_number = 0


    # Create every possible pair of agents
    for agent_a, agent_b in combinations(agents, 2):

        match_number += 1

        print("\n--------------------------------")
        print("Match", match_number)
        print(agent_a, "vs", agent_b)
        print("--------------------------------")


        for game_number in range(
            1,
            games_per_pair + 1
        ):

            # Alternate starting positions
            if game_number % 2 == 1:

                player_1_agent = agent_a
                player_2_agent = agent_b

            else:

                player_1_agent = agent_b
                player_2_agent = agent_a


            # Hide detailed battle output
            hidden_output = io.StringIO()

            with redirect_stdout(hidden_output):

                winner, turns_played, metrics = play_game(
                    max_turns=maximum_turns,
                    player_1_agent=player_1_agent,
                    player_2_agent=player_2_agent
                )


            # Identify the winning agent
            if winner == "Player 1":

                winning_agent = player_1_agent

            elif winner == "Player 2":

                winning_agent = player_2_agent

            else:

                winning_agent = "Draw"


            # Count the result
            if winning_agent == "Draw":

                overall_results[agent_a]["draws"] += 1
                overall_results[agent_b]["draws"] += 1

            else:

                overall_results[winning_agent]["wins"] += 1


            # Read player metrics
            player_1_metrics = metrics["Player 1"]
            player_2_metrics = metrics["Player 2"]


            # Add metrics to the correct agents
            add_agent_metrics(
                player_1_agent,
                player_1_metrics,
                turns_played
            )

            add_agent_metrics(
                player_2_agent,
                player_2_metrics,
                turns_played
            )


            # Save one game to the CSV
            writer.writerow([
                match_number,
                game_number,
                agent_a,
                agent_b,
                player_1_agent,
                player_2_agent,
                winner,
                winning_agent,
                turns_played,

                player_1_metrics["attacks_made"],
                player_1_metrics["successful_attacks"],
                player_1_metrics["armies_lost"],
                player_1_metrics["territories_captured"],
                player_1_metrics["decisions_made"],
                player_1_metrics["decision_time_seconds"],
                player_1_metrics["simulations_run"],

                player_2_metrics["attacks_made"],
                player_2_metrics["successful_attacks"],
                player_2_metrics["armies_lost"],
                player_2_metrics["territories_captured"],
                player_2_metrics["decisions_made"],
                player_2_metrics["decision_time_seconds"],
                player_2_metrics["simulations_run"]
            ])


            print(
                "Game",
                game_number,
                "completed - Winner:",
                winning_agent
            )


# ==================================================
# Display tournament summary
# ==================================================

print("\n================================")
print("Tournament Summary")
print("================================")


for agent_name, results in overall_results.items():

    games = results["games"]
    wins = results["wins"]
    draws = results["draws"]
    attacks = results["attacks"]
    decisions = results["decisions"]


    if games > 0:

        win_rate = (
            wins / games
        ) * 100

        draw_rate = (
            draws / games
        ) * 100

        average_turns = (
            results["total_turns"] / games
        )

        average_attacks = (
            attacks / games
        )

        average_armies_lost = (
            results["armies_lost"] / games
        )

        average_captures = (
            results["territories_captured"] / games
        )

        average_simulations = (
            results["simulations"] / games
        )

    else:

        win_rate = 0
        draw_rate = 0
        average_turns = 0
        average_attacks = 0
        average_armies_lost = 0
        average_captures = 0
        average_simulations = 0


    if attacks > 0:

        attack_success_rate = (
            results["successful_attacks"]
            / attacks
        ) * 100

    else:

        attack_success_rate = 0


    if decisions > 0:

        average_decision_time = (
            results["decision_time"]
            / decisions
        )

    else:

        average_decision_time = 0


    print("\nAgent:", agent_name)
    print("------------------------------")

    print("Games:", games)
    print("Wins:", wins)
    print("Draws:", draws)

    print(
        "Win rate:",
        round(win_rate, 2),
        "%"
    )

    print(
        "Draw rate:",
        round(draw_rate, 2),
        "%"
    )

    print(
        "Average game length:",
        round(average_turns, 2)
    )

    print(
        "Average attacks:",
        round(average_attacks, 2)
    )

    print(
        "Attack success rate:",
        round(attack_success_rate, 2),
        "%"
    )

    print(
        "Average armies lost:",
        round(average_armies_lost, 2)
    )

    print(
        "Average territories captured:",
        round(average_captures, 2)
    )

    print(
        "Average decision time:",
        round(average_decision_time, 6),
        "seconds"
    )

    print(
        "Average simulations:",
        round(average_simulations, 2)
    )


print(
    "\nFull tournament results saved to:",
    csv_file
)