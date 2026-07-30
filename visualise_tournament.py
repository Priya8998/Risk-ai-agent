import csv
import os

import matplotlib.pyplot as plt


# ==================================================
# File locations
# ==================================================

tournament_file = "results/all_agents_tournament.csv"
summary_file = "results/tournament_summary.csv"
graphs_folder = "results/graphs"


# Create the graphs folder
os.makedirs(graphs_folder, exist_ok=True)


# ==================================================
# Store each agent's results
# ==================================================

agent_results = {}


def create_agent_record():

    return {
        "games": 0,
        "wins": 0,
        "draws": 0,
        "attacks": 0,
        "successful_attacks": 0,
        "territories_captured": 0,
        "decisions": 0,
        "decision_time": 0.0,
        "simulations": 0
    }


def add_player_metrics(
    agent_name,
    row,
    player_number
):

    prefix = f"player_{player_number}_"

    agent_results[agent_name]["attacks"] += int(
        row[prefix + "attacks"]
    )

    agent_results[agent_name]["successful_attacks"] += int(
        row[prefix + "successful_attacks"]
    )

    agent_results[agent_name]["territories_captured"] += int(
        row[prefix + "territories_captured"]
    )

    agent_results[agent_name]["decisions"] += int(
        row[prefix + "decisions"]
    )

    agent_results[agent_name]["decision_time"] += float(
        row[prefix + "decision_time"]
    )

    agent_results[agent_name]["simulations"] += int(
        row[prefix + "simulations"]
    )


# ==================================================
# Read tournament results
# ==================================================

with open(
    tournament_file,
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        player_1_agent = row["player_1_agent"]
        player_2_agent = row["player_2_agent"]
        winning_agent = row["winning_agent"]


        # Create records for new agents
        if player_1_agent not in agent_results:
            agent_results[player_1_agent] = create_agent_record()

        if player_2_agent not in agent_results:
            agent_results[player_2_agent] = create_agent_record()


        # Count games
        agent_results[player_1_agent]["games"] += 1
        agent_results[player_2_agent]["games"] += 1


        # Count wins and draws
        if winning_agent == "Draw":

            agent_results[player_1_agent]["draws"] += 1
            agent_results[player_2_agent]["draws"] += 1

        else:

            agent_results[winning_agent]["wins"] += 1


        # Add performance metrics
        add_player_metrics(
            player_1_agent,
            row,
            1
        )

        add_player_metrics(
            player_2_agent,
            row,
            2
        )


# ==================================================
# Calculate final performance values
# ==================================================

summary_results = []


for agent_name, results in agent_results.items():

    games = results["games"]
    attacks = results["attacks"]
    decisions = results["decisions"]


    if games > 0:

        win_rate = (
            results["wins"] / games
        ) * 100

        draw_rate = (
            results["draws"] / games
        ) * 100

        average_captures = (
            results["territories_captured"] / games
        )

        average_simulations = (
            results["simulations"] / games
        )

    else:

        win_rate = 0
        draw_rate = 0
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


    # Convert seconds to milliseconds
    average_decision_time_ms = (
        average_decision_time * 1000
    )


    summary_results.append({
        "agent": agent_name,
        "games": games,
        "wins": results["wins"],
        "draws": results["draws"],
        "win_rate": win_rate,
        "draw_rate": draw_rate,
        "attack_success_rate": attack_success_rate,
        "average_captures": average_captures,
        "average_decision_time_ms": average_decision_time_ms,
        "average_simulations": average_simulations
    })


# Sort agents by win rate
summary_results.sort(
    key=lambda item: item["win_rate"],
    reverse=True
)


# ==================================================
# Save tournament summary CSV
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
        "draws",
        "win_rate",
        "draw_rate",
        "attack_success_rate",
        "average_territories_captured",
        "average_decision_time_ms",
        "average_simulations"
    ])


    for result in summary_results:

        writer.writerow([
            result["agent"],
            result["games"],
            result["wins"],
            result["draws"],
            round(result["win_rate"], 2),
            round(result["draw_rate"], 2),
            round(result["attack_success_rate"], 2),
            round(result["average_captures"], 2),
            round(result["average_decision_time_ms"], 4),
            round(result["average_simulations"], 2)
        ])


# ==================================================
# Prepare information for graphs
# ==================================================

agent_names = [
    result["agent"]
    for result in summary_results
]

win_rates = [
    result["win_rate"]
    for result in summary_results
]

attack_success_rates = [
    result["attack_success_rate"]
    for result in summary_results
]

decision_times = [
    result["average_decision_time_ms"]
    for result in summary_results
]

simulation_counts = [
    result["average_simulations"]
    for result in summary_results
]


# ==================================================
# Graph 1: Win rate
# ==================================================

plt.figure(figsize=(10, 6))

plt.bar(
    agent_names,
    win_rates
)

plt.title("AI Agent Win Rate")
plt.xlabel("Agent")
plt.ylabel("Win Rate (%)")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    f"{graphs_folder}/win_rate.png",
    dpi=300
)

plt.close()


# ==================================================
# Graph 2: Attack success rate
# ==================================================

plt.figure(figsize=(10, 6))

plt.bar(
    agent_names,
    attack_success_rates
)

plt.title("AI Agent Attack Success Rate")
plt.xlabel("Agent")
plt.ylabel("Attack Success Rate (%)")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    f"{graphs_folder}/attack_success_rate.png",
    dpi=300
)

plt.close()


# ==================================================
# Graph 3: Decision time
# ==================================================

plt.figure(figsize=(10, 6))

plt.bar(
    agent_names,
    decision_times
)

plt.title("Average Agent Decision Time")
plt.xlabel("Agent")
plt.ylabel("Average Decision Time (milliseconds)")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    f"{graphs_folder}/decision_time.png",
    dpi=300
)

plt.close()


# ==================================================
# Graph 4: Simulation cost
# ==================================================

plt.figure(figsize=(10, 6))

plt.bar(
    agent_names,
    simulation_counts
)

plt.title("Average Simulations Per Game")
plt.xlabel("Agent")
plt.ylabel("Simulations")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    f"{graphs_folder}/simulation_cost.png",
    dpi=300
)

plt.close()


# ==================================================
# Display summary
# ==================================================

print("\n================================")
print("Tournament Visualisation Complete")
print("================================")

for result in summary_results:

    print("\nAgent:", result["agent"])

    print(
        "Win rate:",
        round(result["win_rate"], 2),
        "%"
    )

    print(
        "Attack success rate:",
        round(result["attack_success_rate"], 2),
        "%"
    )

    print(
        "Average decision time:",
        round(result["average_decision_time_ms"], 4),
        "milliseconds"
    )

    print(
        "Average simulations:",
        round(result["average_simulations"], 2)
    )


print("\nSummary saved to:", summary_file)
print("Graphs saved inside:", graphs_folder)