import csv


# Change this when analysing another comparison
csv_file = (
    "results/"
    "monte_carlo_agent_vs_heuristic_agent.csv"
)


# Store combined agent results
agent_results = {}


# Create an empty record for one agent
def create_agent_record():

    return {
        "games": 0,
        "wins": 0,
        "attacks": 0,
        "successful_attacks": 0,
        "armies_lost": 0,
        "territories_captured": 0,
        "decisions": 0,
        "decision_time": 0.0,
        "simulations": 0
    }


# Add one player's CSV metrics to an agent
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

    agent_results[agent_name]["armies_lost"] += int(
        row[prefix + "armies_lost"]
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


# Read the CSV
with open(
    csv_file,
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

            agent_results[player_1_agent] = (
                create_agent_record()
            )

        if player_2_agent not in agent_results:

            agent_results[player_2_agent] = (
                create_agent_record()
            )


        # Count games
        agent_results[player_1_agent]["games"] += 1
        agent_results[player_2_agent]["games"] += 1


        # Count wins
        if winning_agent != "Draw":

            agent_results[winning_agent]["wins"] += 1


        # Add both players' performance
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
# Display performance summary
# ==================================================

print("\n======================================")
print("Agent Performance Summary")
print("======================================")


for agent_name, results in agent_results.items():

    games = results["games"]
    wins = results["wins"]
    attacks = results["attacks"]
    successful_attacks = results[
        "successful_attacks"
    ]

    decisions = results["decisions"]
    total_decision_time = results[
        "decision_time"
    ]

    win_rate = (
        wins / games
    ) * 100


    if attacks > 0:

        attack_success_rate = (
            successful_attacks / attacks
        ) * 100

    else:

        attack_success_rate = 0


    if decisions > 0:

        average_decision_time = (
            total_decision_time / decisions
        )

    else:

        average_decision_time = 0


    average_attacks = (
        attacks / games
    )

    average_armies_lost = (
        results["armies_lost"] / games
    )

    average_territories_captured = (
        results["territories_captured"] / games
    )

    average_simulations = (
        results["simulations"] / games
    )


    print("\nAgent:", agent_name)
    print("------------------------------")

    print("Games:", games)
    print("Wins:", wins)

    print(
        "Win rate:",
        round(win_rate, 2),
        "%"
    )

    print(
        "Average attacks per game:",
        round(average_attacks, 2)
    )

    print(
        "Attack success rate:",
        round(attack_success_rate, 2),
        "%"
    )

    print(
        "Average armies lost per game:",
        round(average_armies_lost, 2)
    )

    print(
        "Average territories captured:",
        round(average_territories_captured, 2)
    )

    print(
        "Average decision time:",
        round(average_decision_time, 6),
        "seconds"
    )

    print(
        "Average simulations per game:",
        round(average_simulations, 2)
    )