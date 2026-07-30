import csv
import io
import os
import platform
import sys
import time

from contextlib import redirect_stdout
from itertools import combinations

from risk_game import play_game


# ==================================================
# 1. Final experiment settings
# ==================================================

agents = [
    "Random Agent",
    "Rule-Based Agent",
    "Heuristic Agent",
    "Monte Carlo Agent"
]

# Final high-volume setting
games_per_pair = 500

# Maximum turns allowed in each game
maximum_turns = 100

# Fixed base seed
base_seed = 20260730

# Monte Carlo configuration used in risk_game.py
monte_carlo_simulations_per_attack = 100


# ==================================================
# 2. Create result files
# ==================================================

os.makedirs("results", exist_ok=True)

csv_file = (
    "results/"
    "final_reproducible_tournament.csv"
)

config_file = (
    "results/"
    "final_evaluation_config.txt"
)


# Four agents create six different pairings
number_of_pairs = 6

total_expected_games = (
    number_of_pairs * games_per_pair
)


# ==================================================
# 3. Store tournament totals
# ==================================================

overall_results = {}

for agent_name in agents:

    overall_results[agent_name] = {
        "games": 0,
        "wins": 0,
        "draws": 0
    }


# ==================================================
# 4. Save experiment configuration
# ==================================================

with open(
    config_file,
    "w",
    encoding="utf-8"
) as file:

    file.write("RISK AI Final Evaluation Configuration\n")
    file.write("======================================\n")

    file.write(
        f"Agents: {', '.join(agents)}\n"
    )

    file.write(
        f"Games per pair: {games_per_pair}\n"
    )

    file.write(
        f"Number of pairings: {number_of_pairs}\n"
    )

    file.write(
        f"Total games: {total_expected_games}\n"
    )

    file.write(
        f"Maximum turns: {maximum_turns}\n"
    )

    file.write(
        f"Base random seed: {base_seed}\n"
    )

    file.write(
        "Monte Carlo simulations per attack: "
        f"{monte_carlo_simulations_per_attack}\n"
    )

    file.write(
        f"Python version: {sys.version}\n"
    )

    file.write(
        f"Operating system: {platform.platform()}\n"
    )


# ==================================================
# 5. Start the final evaluation
# ==================================================

print("\n========================================")
print("Final Reproducible RISK AI Evaluation")
print("========================================")

print("Agents:", agents)
print("Games per pair:", games_per_pair)
print("Total pairings:", number_of_pairs)
print("Total games:", total_expected_games)
print("Base seed:", base_seed)

print("\nThis may take several minutes.")

evaluation_start_time = time.perf_counter()


# ==================================================
# 6. Create the raw-results CSV
# ==================================================

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
        "global_game_number",
        "random_seed",

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
    global_game_number = 0


    # Create all possible pairs
    for agent_a, agent_b in combinations(
        agents,
        2
    ):

        match_number += 1

        print("\n----------------------------------------")
        print("Match", match_number)
        print(agent_a, "vs", agent_b)
        print("----------------------------------------")


        # Run all games for this pair
        for game_number in range(
            1,
            games_per_pair + 1
        ):

            global_game_number += 1


            # Alternate starting positions
            if game_number % 2 == 1:

                player_1_agent = agent_a
                player_2_agent = agent_b

            else:

                player_1_agent = agent_b
                player_2_agent = agent_a


            # Create one unique and repeatable seed
            game_seed = (
                base_seed
                + match_number * 100000
                + game_number
            )


            # Hide detailed battle output
            hidden_output = io.StringIO()

            with redirect_stdout(hidden_output):

                (
                    winner,
                    turns_played,
                    metrics
                ) = play_game(
                    max_turns=maximum_turns,
                    player_1_agent=player_1_agent,
                    player_2_agent=player_2_agent,
                    random_seed=game_seed
                )


            # Identify the winning agent
            if winner == "Player 1":

                winning_agent = player_1_agent

            elif winner == "Player 2":

                winning_agent = player_2_agent

            else:

                winning_agent = "Draw"


            # Update overall results
            overall_results[
                player_1_agent
            ]["games"] += 1

            overall_results[
                player_2_agent
            ]["games"] += 1


            if winning_agent == "Draw":

                overall_results[
                    player_1_agent
                ]["draws"] += 1

                overall_results[
                    player_2_agent
                ]["draws"] += 1

            else:

                overall_results[
                    winning_agent
                ]["wins"] += 1


            # Read player metrics
            player_1_metrics = metrics["Player 1"]
            player_2_metrics = metrics["Player 2"]


            # Save the full game result
            writer.writerow([
                match_number,
                game_number,
                global_game_number,
                game_seed,

                agent_a,
                agent_b,

                player_1_agent,
                player_2_agent,

                winner,
                winning_agent,
                turns_played,

                player_1_metrics[
                    "attacks_made"
                ],

                player_1_metrics[
                    "successful_attacks"
                ],

                player_1_metrics[
                    "armies_lost"
                ],

                player_1_metrics[
                    "territories_captured"
                ],

                player_1_metrics[
                    "decisions_made"
                ],

                player_1_metrics[
                    "decision_time_seconds"
                ],

                player_1_metrics[
                    "simulations_run"
                ],

                player_2_metrics[
                    "attacks_made"
                ],

                player_2_metrics[
                    "successful_attacks"
                ],

                player_2_metrics[
                    "armies_lost"
                ],

                player_2_metrics[
                    "territories_captured"
                ],

                player_2_metrics[
                    "decisions_made"
                ],

                player_2_metrics[
                    "decision_time_seconds"
                ],

                player_2_metrics[
                    "simulations_run"
                ]
            ])


            # Save the row immediately
            file.flush()


            # Show progress every 25 games
            if (
                game_number % 25 == 0
                or game_number == games_per_pair
            ):

                print(
                    "Completed",
                    game_number,
                    "of",
                    games_per_pair,
                    "games"
                )


# ==================================================
# 7. Calculate total running time
# ==================================================

evaluation_end_time = time.perf_counter()

total_evaluation_time = (
    evaluation_end_time
    - evaluation_start_time
)


# ==================================================
# 8. Display the final summary
# ==================================================

print("\n========================================")
print("Final Evaluation Summary")
print("========================================")

for agent_name, results in overall_results.items():

    games = results["games"]
    wins = results["wins"]
    draws = results["draws"]

    if games > 0:

        win_rate = (
            wins / games
        ) * 100

        draw_rate = (
            draws / games
        ) * 100

    else:

        win_rate = 0
        draw_rate = 0


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


print("\nTotal games:", total_expected_games)

print(
    "Total evaluation time:",
    round(total_evaluation_time, 2),
    "seconds"
)

print(
    "\nRaw results saved to:",
    csv_file
)

print(
    "Configuration saved to:",
    config_file
)