import csv
import math
import os
import statistics

import matplotlib.pyplot as plt


# ==================================================
# 1. File locations
# ==================================================

raw_results_file = (
    "results/final_reproducible_tournament.csv"
)

summary_file = (
    "results/final_agent_summary.csv"
)

head_to_head_file = (
    "results/final_head_to_head_summary.csv"
)

position_file = (
    "results/final_starting_position_summary.csv"
)

reproducibility_file = (
    "results/reproducibility_report.txt"
)

graphs_folder = "results/final_graphs"


# Create the final graphs folder
os.makedirs(graphs_folder, exist_ok=True)


# Check that the final tournament file exists
if not os.path.exists(raw_results_file):

    raise FileNotFoundError(
        "The final tournament file was not found. "
        "Run final_evaluation.py first."
    )


# ==================================================
# 2. Helper functions
# ==================================================

def create_agent_record():

    return {
        "games": 0,
        "wins": 0,
        "losses": 0,
        "draws": 0,

        "turns": [],

        "attacks": 0,
        "successful_attacks": 0,
        "armies_lost": 0,
        "territories_captured": 0,

        "decisions": 0,
        "decision_time": 0.0,
        "simulations": 0,

        "player_1_games": 0,
        "player_1_wins": 0,

        "player_2_games": 0,
        "player_2_wins": 0
    }


def create_pair_record(agent_1, agent_2):

    return {
        "agent_1": agent_1,
        "agent_2": agent_2,
        "games": 0,
        "agent_1_wins": 0,
        "agent_2_wins": 0,
        "draws": 0
    }


# Calculate a 95% Wilson confidence interval
def wilson_confidence_interval(
    successes,
    total,
    z_value=1.96
):

    if total == 0:
        return 0, 0

    probability = successes / total

    denominator = (
        1
        + (z_value ** 2 / total)
    )

    centre = (
        probability
        + (z_value ** 2 / (2 * total))
    )

    margin = z_value * math.sqrt(
        (
            probability * (1 - probability)
            + z_value ** 2 / (4 * total)
        )
        / total
    )

    lower = (
        centre - margin
    ) / denominator

    upper = (
        centre + margin
    ) / denominator

    return lower * 100, upper * 100


# Add one player's metrics to the correct agent
def add_player_metrics(
    agent_name,
    row,
    player_number,
    turns_played,
    agent_results
):

    prefix = f"player_{player_number}_"

    results = agent_results[agent_name]

    results["games"] += 1
    results["turns"].append(turns_played)

    results["attacks"] += int(
        row[prefix + "attacks"]
    )

    results["successful_attacks"] += int(
        row[prefix + "successful_attacks"]
    )

    results["armies_lost"] += int(
        row[prefix + "armies_lost"]
    )

    results["territories_captured"] += int(
        row[prefix + "territories_captured"]
    )

    results["decisions"] += int(
        row[prefix + "decisions"]
    )

    results["decision_time"] += float(
        row[prefix + "decision_time"]
    )

    results["simulations"] += int(
        row[prefix + "simulations"]
    )


# ==================================================
# 3. Read the final tournament data
# ==================================================

agent_results = {}
pair_results = {}

all_seeds = []
total_games = 0

player_1_wins = 0
player_2_wins = 0
total_draws = 0


with open(
    raw_results_file,
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        total_games += 1

        player_1_agent = row["player_1_agent"]
        player_2_agent = row["player_2_agent"]

        winning_agent = row["winning_agent"]
        winner_player = row["winner_player"]

        turns_played = int(
            row["turns_played"]
        )

        random_seed = int(
            row["random_seed"]
        )

        all_seeds.append(random_seed)


        # Create agent records when required
        if player_1_agent not in agent_results:

            agent_results[player_1_agent] = (
                create_agent_record()
            )

        if player_2_agent not in agent_results:

            agent_results[player_2_agent] = (
                create_agent_record()
            )


        # Add Player 1 performance
        add_player_metrics(
            player_1_agent,
            row,
            1,
            turns_played,
            agent_results
        )

        # Add Player 2 performance
        add_player_metrics(
            player_2_agent,
            row,
            2,
            turns_played,
            agent_results
        )


        # Count starting-position games
        agent_results[
            player_1_agent
        ]["player_1_games"] += 1

        agent_results[
            player_2_agent
        ]["player_2_games"] += 1


        # Count wins, losses and draws
        if winning_agent == "Draw":

            agent_results[
                player_1_agent
            ]["draws"] += 1

            agent_results[
                player_2_agent
            ]["draws"] += 1

            total_draws += 1

        else:

            agent_results[
                winning_agent
            ]["wins"] += 1

            if winning_agent == player_1_agent:

                losing_agent = player_2_agent

            else:

                losing_agent = player_1_agent

            agent_results[
                losing_agent
            ]["losses"] += 1


        # Count first-player and second-player wins
        if winner_player == "Player 1":

            player_1_wins += 1

            agent_results[
                player_1_agent
            ]["player_1_wins"] += 1

        elif winner_player == "Player 2":

            player_2_wins += 1

            agent_results[
                player_2_agent
            ]["player_2_wins"] += 1


        # Create a consistent head-to-head pair
        pair_agents = sorted([
            player_1_agent,
            player_2_agent
        ])

        pair_key = (
            pair_agents[0],
            pair_agents[1]
        )


        if pair_key not in pair_results:

            pair_results[pair_key] = (
                create_pair_record(
                    pair_agents[0],
                    pair_agents[1]
                )
            )


        pair_record = pair_results[pair_key]

        pair_record["games"] += 1


        if winning_agent == "Draw":

            pair_record["draws"] += 1

        elif winning_agent == pair_record["agent_1"]:

            pair_record["agent_1_wins"] += 1

        elif winning_agent == pair_record["agent_2"]:

            pair_record["agent_2_wins"] += 1


# ==================================================
# 4. Calculate the final agent summary
# ==================================================

final_summary = []


for agent_name, results in agent_results.items():

    games = results["games"]
    wins = results["wins"]
    losses = results["losses"]
    draws = results["draws"]

    attacks = results["attacks"]
    decisions = results["decisions"]


    # Basic outcome rates
    win_rate = (
        wins / games
    ) * 100

    loss_rate = (
        losses / games
    ) * 100

    draw_rate = (
        draws / games
    ) * 100


    # Win-rate confidence interval
    (
        confidence_lower,
        confidence_upper
    ) = wilson_confidence_interval(
        wins,
        games
    )


    # Game length metrics
    average_turns = statistics.mean(
        results["turns"]
    )

    median_turns = statistics.median(
        results["turns"]
    )

    minimum_turns = min(
        results["turns"]
    )

    maximum_turns = max(
        results["turns"]
    )


    if len(results["turns"]) > 1:

        turn_standard_deviation = (
            statistics.stdev(
                results["turns"]
            )
        )

    else:

        turn_standard_deviation = 0


    # Attack success rate
    if attacks > 0:

        attack_success_rate = (
            results["successful_attacks"]
            / attacks
        ) * 100

    else:

        attack_success_rate = 0


    # Decision-time metric
    if decisions > 0:

        average_decision_time_ms = (
            results["decision_time"]
            / decisions
        ) * 1000

    else:

        average_decision_time_ms = 0


    # Average performance per game
    average_attacks = (
        attacks / games
    )

    average_armies_lost = (
        results["armies_lost"] / games
    )

    average_captures = (
        results["territories_captured"]
        / games
    )

    average_simulations = (
        results["simulations"] / games
    )


    # Starting-position performance
    if results["player_1_games"] > 0:

        player_1_win_rate = (
            results["player_1_wins"]
            / results["player_1_games"]
        ) * 100

    else:

        player_1_win_rate = 0


    if results["player_2_games"] > 0:

        player_2_win_rate = (
            results["player_2_wins"]
            / results["player_2_games"]
        ) * 100

    else:

        player_2_win_rate = 0


    final_summary.append({

        "agent": agent_name,

        "games": games,
        "wins": wins,
        "losses": losses,
        "draws": draws,

        "win_rate": win_rate,
        "loss_rate": loss_rate,
        "draw_rate": draw_rate,

        "confidence_lower": confidence_lower,
        "confidence_upper": confidence_upper,

        "average_turns": average_turns,
        "median_turns": median_turns,
        "turn_standard_deviation": (
            turn_standard_deviation
        ),
        "minimum_turns": minimum_turns,
        "maximum_turns": maximum_turns,

        "average_attacks": average_attacks,
        "attack_success_rate": (
            attack_success_rate
        ),
        "average_armies_lost": (
            average_armies_lost
        ),
        "average_captures": (
            average_captures
        ),

        "average_decision_time_ms": (
            average_decision_time_ms
        ),

        "average_simulations": (
            average_simulations
        ),

        "player_1_win_rate": (
            player_1_win_rate
        ),

        "player_2_win_rate": (
            player_2_win_rate
        )
    })


# Sort agents from highest to lowest win rate
final_summary.sort(
    key=lambda result: result["win_rate"],
    reverse=True
)


# ==================================================
# 5. Save the final agent summary
# ==================================================

with open(
    summary_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "agent",

        "games",
        "wins",
        "losses",
        "draws",

        "win_rate",
        "loss_rate",
        "draw_rate",

        "win_rate_ci_lower",
        "win_rate_ci_upper",

        "average_turns",
        "median_turns",
        "turn_standard_deviation",
        "minimum_turns",
        "maximum_turns",

        "average_attacks",
        "attack_success_rate",
        "average_armies_lost",
        "average_territories_captured",

        "average_decision_time_ms",
        "average_simulations_per_game",

        "player_1_win_rate",
        "player_2_win_rate"
    ])


    for result in final_summary:

        writer.writerow([
            result["agent"],

            result["games"],
            result["wins"],
            result["losses"],
            result["draws"],

            round(result["win_rate"], 2),
            round(result["loss_rate"], 2),
            round(result["draw_rate"], 2),

            round(result["confidence_lower"], 2),
            round(result["confidence_upper"], 2),

            round(result["average_turns"], 2),
            round(result["median_turns"], 2),
            round(
                result["turn_standard_deviation"],
                2
            ),
            result["minimum_turns"],
            result["maximum_turns"],

            round(result["average_attacks"], 2),
            round(
                result["attack_success_rate"],
                2
            ),
            round(
                result["average_armies_lost"],
                2
            ),
            round(
                result["average_captures"],
                2
            ),

            round(
                result[
                    "average_decision_time_ms"
                ],
                6
            ),

            round(
                result["average_simulations"],
                2
            ),

            round(
                result["player_1_win_rate"],
                2
            ),

            round(
                result["player_2_win_rate"],
                2
            )
        ])


# ==================================================
# 6. Save head-to-head results
# ==================================================

with open(
    head_to_head_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "agent_1",
        "agent_2",
        "games",
        "agent_1_wins",
        "agent_2_wins",
        "draws",
        "agent_1_win_rate",
        "agent_2_win_rate",
        "draw_rate"
    ])


    for pair_record in pair_results.values():

        games = pair_record["games"]

        agent_1_win_rate = (
            pair_record["agent_1_wins"]
            / games
        ) * 100

        agent_2_win_rate = (
            pair_record["agent_2_wins"]
            / games
        ) * 100

        draw_rate = (
            pair_record["draws"]
            / games
        ) * 100


        writer.writerow([
            pair_record["agent_1"],
            pair_record["agent_2"],
            games,
            pair_record["agent_1_wins"],
            pair_record["agent_2_wins"],
            pair_record["draws"],
            round(agent_1_win_rate, 2),
            round(agent_2_win_rate, 2),
            round(draw_rate, 2)
        ])


# ==================================================
# 7. Save starting-position summary
# ==================================================

decisive_games = (
    player_1_wins + player_2_wins
)


if decisive_games > 0:

    first_player_decisive_win_rate = (
        player_1_wins / decisive_games
    ) * 100

else:

    first_player_decisive_win_rate = 0


overall_first_player_win_rate = (
    player_1_wins / total_games
) * 100

overall_second_player_win_rate = (
    player_2_wins / total_games
) * 100

overall_draw_rate = (
    total_draws / total_games
) * 100


with open(
    position_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "total_games",
        "player_1_wins",
        "player_2_wins",
        "draws",
        "player_1_win_rate",
        "player_2_win_rate",
        "draw_rate",
        "player_1_win_rate_decisive_games"
    ])

    writer.writerow([
        total_games,
        player_1_wins,
        player_2_wins,
        total_draws,
        round(
            overall_first_player_win_rate,
            2
        ),
        round(
            overall_second_player_win_rate,
            2
        ),
        round(overall_draw_rate, 2),
        round(
            first_player_decisive_win_rate,
            2
        )
    ])


# ==================================================
# 8. Save reproducibility report
# ==================================================

unique_seeds = set(all_seeds)

duplicate_seed_count = (
    len(all_seeds) - len(unique_seeds)
)


with open(
    reproducibility_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "RISK AI Reproducibility Report\n"
    )

    file.write(
        "==============================\n"
    )

    file.write(
        f"Total games: {total_games}\n"
    )

    file.write(
        f"Seeds recorded: {len(all_seeds)}\n"
    )

    file.write(
        f"Unique seeds: {len(unique_seeds)}\n"
    )

    file.write(
        "Duplicate seed count: "
        f"{duplicate_seed_count}\n"
    )

    file.write(
        f"Minimum seed: {min(all_seeds)}\n"
    )

    file.write(
        f"Maximum seed: {max(all_seeds)}\n"
    )

    if duplicate_seed_count == 0:

        file.write(
            "Seed validation: PASSED\n"
        )

    else:

        file.write(
            "Seed validation: FAILED\n"
        )

    file.write(
        "\nGame outcomes and game-state metrics "
        "are reproducible when the same seeds "
        "and code version are used.\n"
    )

    file.write(
        "Decision-time values may vary slightly "
        "because they depend on computer workload.\n"
    )


# ==================================================
# 9. Prepare values for graphs
# ==================================================

agent_names = [
    result["agent"]
    for result in final_summary
]

win_rates = [
    result["win_rate"]
    for result in final_summary
]

confidence_lower_errors = [
    result["win_rate"]
    - result["confidence_lower"]
    for result in final_summary
]

confidence_upper_errors = [
    result["confidence_upper"]
    - result["win_rate"]
    for result in final_summary
]

draw_rates = [
    result["draw_rate"]
    for result in final_summary
]

attack_success_rates = [
    result["attack_success_rate"]
    for result in final_summary
]

decision_times = [
    result["average_decision_time_ms"]
    for result in final_summary
]

simulation_counts = [
    result["average_simulations"]
    for result in final_summary
]

player_1_agent_rates = [
    result["player_1_win_rate"]
    for result in final_summary
]

player_2_agent_rates = [
    result["player_2_win_rate"]
    for result in final_summary
]


# ==================================================
# 10. Graph: win rate with confidence intervals
# ==================================================

plt.figure(figsize=(10, 6))

positions = list(
    range(len(agent_names))
)

plt.bar(
    positions,
    win_rates
)

plt.errorbar(
    positions,
    win_rates,
    yerr=[
        confidence_lower_errors,
        confidence_upper_errors
    ],
    fmt="none",
    capsize=5
)

plt.title(
    "Agent Win Rate with 95% Confidence Intervals"
)

plt.xlabel("AI Agent")
plt.ylabel("Win Rate (%)")

plt.xticks(
    positions,
    agent_names,
    rotation=20
)

plt.tight_layout()

plt.savefig(
    f"{graphs_folder}/"
    "win_rate_confidence_intervals.png",
    dpi=300
)

plt.close()


# ==================================================
# 11. Graph: draw rate
# ==================================================

plt.figure(figsize=(10, 6))

plt.bar(
    agent_names,
    draw_rates
)

plt.title("Agent Draw Rate")
plt.xlabel("AI Agent")
plt.ylabel("Draw Rate (%)")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    f"{graphs_folder}/draw_rate.png",
    dpi=300
)

plt.close()


# ==================================================
# 12. Graph: attack success rate
# ==================================================

plt.figure(figsize=(10, 6))

plt.bar(
    agent_names,
    attack_success_rates
)

plt.title("Agent Attack Success Rate")
plt.xlabel("AI Agent")
plt.ylabel("Attack Success Rate (%)")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    f"{graphs_folder}/attack_success_rate.png",
    dpi=300
)

plt.close()


# ==================================================
# 13. Graph: average decision time
# ==================================================

plt.figure(figsize=(10, 6))

plt.bar(
    agent_names,
    decision_times
)

plt.title("Average Agent Decision Time")
plt.xlabel("AI Agent")
plt.ylabel("Decision Time (milliseconds)")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    f"{graphs_folder}/decision_time.png",
    dpi=300
)

plt.close()


# ==================================================
# 14. Graph: simulations per game
# ==================================================

plt.figure(figsize=(10, 6))

plt.bar(
    agent_names,
    simulation_counts
)

plt.title("Average Simulations Per Game")
plt.xlabel("AI Agent")
plt.ylabel("Simulations")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    f"{graphs_folder}/simulations_per_game.png",
    dpi=300
)

plt.close()


# ==================================================
# 15. Graph: Player 1 versus Player 2 performance
# ==================================================

bar_width = 0.35

player_1_positions = [
    position - bar_width / 2
    for position in positions
]

player_2_positions = [
    position + bar_width / 2
    for position in positions
]


plt.figure(figsize=(10, 6))

plt.bar(
    player_1_positions,
    player_1_agent_rates,
    width=bar_width,
    label="Playing as Player 1"
)

plt.bar(
    player_2_positions,
    player_2_agent_rates,
    width=bar_width,
    label="Playing as Player 2"
)

plt.title(
    "Agent Performance by Starting Position"
)

plt.xlabel("AI Agent")
plt.ylabel("Win Rate (%)")

plt.xticks(
    positions,
    agent_names,
    rotation=20
)

plt.legend()
plt.tight_layout()

plt.savefig(
    f"{graphs_folder}/"
    "starting_position_comparison.png",
    dpi=300
)

plt.close()


# ==================================================
# 16. Display the final results
# ==================================================

print("\n========================================")
print("Final Statistical Analysis Complete")
print("========================================")

print("\nTotal games analysed:", total_games)

print(
    "Unique random seeds:",
    len(unique_seeds)
)

print(
    "Duplicate seeds:",
    duplicate_seed_count
)


for result in final_summary:

    print("\nAgent:", result["agent"])
    print("------------------------------")

    print(
        "Win rate:",
        round(result["win_rate"], 2),
        "%"
    )

    print(
        "95% confidence interval:",
        round(
            result["confidence_lower"],
            2
        ),
        "%",
        "to",
        round(
            result["confidence_upper"],
            2
        ),
        "%"
    )

    print(
        "Draw rate:",
        round(result["draw_rate"], 2),
        "%"
    )

    print(
        "Average game length:",
        round(result["average_turns"], 2)
    )

    print(
        "Attack success rate:",
        round(
            result["attack_success_rate"],
            2
        ),
        "%"
    )

    print(
        "Average decision time:",
        round(
            result[
                "average_decision_time_ms"
            ],
            6
        ),
        "milliseconds"
    )


print("\nStarting-position results")
print("------------------------------")

print("Player 1 wins:", player_1_wins)
print("Player 2 wins:", player_2_wins)
print("Draws:", total_draws)

print(
    "Player 1 win rate:",
    round(
        overall_first_player_win_rate,
        2
    ),
    "%"
)

print(
    "Player 2 win rate:",
    round(
        overall_second_player_win_rate,
        2
    ),
    "%"
)


print("\nFiles created:")

print(summary_file)
print(head_to_head_file)
print(position_file)
print(reproducibility_file)
print(graphs_folder)