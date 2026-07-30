import random
import copy
import time

from agents.random_agent import (
    choose_random_reinforcement,
    choose_random_attack
)

from agents.rule_based_agent import (
    choose_rule_reinforcement,
    choose_rule_attack
)

from agents.heuristic_agent import (
    choose_heuristic_reinforcement,
    choose_heuristic_attack
)

from agents.monte_carlo_agent import (
    choose_monte_carlo_reinforcement,
    choose_monte_carlo_attack
)

# List of players in the game
players = ["Player 1", "Player 2"]


# The game map
territories = {
    "A": {
        "owner": "Player 1",
        "armies": 3,
        "neighbours": ["B", "C"]
    },

    "B": {
        "owner": "Player 1",
        "armies": 3,
        "neighbours": ["A", "C", "D"]
    },

    "C": {
        "owner": "Player 1",
        "armies": 3,
        "neighbours": ["A", "B", "E"]
    },

    "D": {
        "owner": "Player 2",
        "armies": 3,
        "neighbours": ["B", "E", "F"]
    },

    "E": {
        "owner": "Player 2",
        "armies": 3,
        "neighbours": ["C", "D", "F"]
    },

    "F": {
        "owner": "Player 2",
        "armies": 3,
        "neighbours": ["D", "E"]
    }
}

# Save the original starting state of the game
starting_territories = copy.deepcopy(territories)

# Store performance information for one game
game_metrics = {
    "Player 1": {
        "attacks_made": 0,
        "successful_attacks": 0,
        "armies_lost": 0,
        "territories_captured": 0,
        "decisions_made": 0,
        "decision_time_seconds": 0.0,
        "simulations_run": 0
    },

    "Player 2": {
        "attacks_made": 0,
        "successful_attacks": 0,
        "armies_lost": 0,
        "territories_captured": 0,
        "decisions_made": 0,
        "decision_time_seconds": 0.0,
        "simulations_run": 0
    }
}

# Find all territories owned by one player
def get_player_territories(player_name):

    player_territories = []

    for territory_name, territory_data in territories.items():

        if territory_data["owner"] == player_name:
            player_territories.append(territory_name)

    return player_territories

# Find all valid attacks for one player
def get_valid_attacks(player_name):

    valid_attacks = []

    # Check every territory on the map
    for territory_name, territory_data in territories.items():

        # Check whether the player owns this territory
        if territory_data["owner"] == player_name:

            # The territory needs more than one army to attack
            if territory_data["armies"] > 1:

                # Check each neighbouring territory
                for neighbour_name in territory_data["neighbours"]:

                    neighbour_data = territories[neighbour_name]

                    # The neighbour must belong to another player
                    if neighbour_data["owner"] != player_name:

                        attack = (territory_name, neighbour_name)
                        valid_attacks.append(attack)

    return valid_attacks

# Calculate how many new armies a player receives
def calculate_reinforcements(player_name):

    player_territories = get_player_territories(player_name)

    territory_count = len(player_territories)

    reinforcements = territory_count // 3

    # Our small map gives at least 1 reinforcement army
    if reinforcements < 1:
        reinforcements = 1

    return reinforcements

# Add reinforcement armies to one territory
def reinforce_territory(player_name, territory_name, armies):

    # Check that the territory exists
    if territory_name not in territories:
        print("Territory does not exist.")
        return False

    # Check that the player owns the territory
    if territories[territory_name]["owner"] != player_name:
        print(player_name, "does not own territory", territory_name)
        return False

    # Check that the number of armies is valid
    if armies <= 0:
        print("The number of armies must be greater than zero.")
        return False

    territories[territory_name]["armies"] += armies

    print(
        player_name,
        "added",
        armies,
        "armies to territory",
        territory_name
    )

    return True

# Roll dice and return the results
def roll_dice(number_of_dice):

    dice_results = []

    for dice in range(number_of_dice):

        result = random.randint(1, 6)

        dice_results.append(result)

    # Put the highest dice first
    dice_results.sort(reverse=True)

    return dice_results

# Compare attacker and defender dice
def compare_dice(attacker_dice, defender_dice):

    attacker_losses = 0
    defender_losses = 0

    # Compare only the dice available on both sides
    number_of_comparisons = min(
        len(attacker_dice),
        len(defender_dice)
    )

    for position in range(number_of_comparisons):

        attacker_result = attacker_dice[position]
        defender_result = defender_dice[position]

        print(
            "Attacker rolled",
            attacker_result,
            "- Defender rolled",
            defender_result
        )

        # Attacker wins only when its die is higher
        if attacker_result > defender_result:
            defender_losses += 1
            print("Defender loses 1 army.")

        else:
            attacker_losses += 1
            print("Attacker loses 1 army.")

    return attacker_losses, defender_losses

# Perform one complete attack round
def attack_territory(attacking_territory, defending_territory):

    # Check that both territories exist
    if attacking_territory not in territories:
        print("Attacking territory does not exist.")
        return False

    if defending_territory not in territories:
        print("Defending territory does not exist.")
        return False

    attacker_data = territories[attacking_territory]
    defender_data = territories[defending_territory]

    attacker_name = attacker_data["owner"]
    defender_name = defender_data["owner"]

    # The territories must be neighbours
    if defending_territory not in attacker_data["neighbours"]:
        print("These territories are not neighbours.")
        return False

    # A player cannot attack their own territory
    if attacker_name == defender_name:
        print("A player cannot attack their own territory.")
        return False

    # At least one army must remain behind
    if attacker_data["armies"] <= 1:
        print("Not enough armies to attack.")
        return False

    print(
        "\n",
        attacker_name,
        "attacks from",
        attacking_territory,
        "to",
        defending_territory
    )

    # Count this attack
    game_metrics[attacker_name]["attacks_made"] += 1

    # Attacker can roll a maximum of 3 dice
    attacker_dice_count = min(
        3,
        attacker_data["armies"] - 1
    )

    # Defender can roll a maximum of 2 dice
    defender_dice_count = min(
        2,
        defender_data["armies"]
    )

    attacker_dice = roll_dice(attacker_dice_count)
    defender_dice = roll_dice(defender_dice_count)

    print("Attacker dice:", attacker_dice)
    print("Defender dice:", defender_dice)

    attacker_losses, defender_losses = compare_dice(
        attacker_dice,
        defender_dice
    )

    # Record armies lost by both players
    game_metrics[attacker_name]["armies_lost"] += attacker_losses
    game_metrics[defender_name]["armies_lost"] += defender_losses

    # The attack is successful if the defender loses an army
    if defender_losses > 0:
        game_metrics[attacker_name]["successful_attacks"] += 1

    # Remove the lost armies
    attacker_data["armies"] -= attacker_losses
    defender_data["armies"] -= defender_losses

    print("\nArmies after battle")
    print(
        attacking_territory,
        "armies:",
        attacker_data["armies"]
    )
    print(
        defending_territory,
        "armies:",
        defender_data["armies"]
    )

    # Check whether the territory was captured
    if defender_data["armies"] == 0:

        # Count the captured territory
        game_metrics[attacker_name]["territories_captured"] += 1

        defender_data["owner"] = attacker_name

        # Move one army into the captured territory
        attacker_data["armies"] -= 1    
        defender_data["armies"] = 1

        print(
            "\n",
            attacker_name,
            "captured territory",
            defending_territory
        )

        return True

    print("\nTerritory was not captured.")

    return False

# Check whether one player owns every territory
def check_winner():

    owners = []

    # Collect the owners of all territories
    for territory_data in territories.values():

        owner = territory_data["owner"]

        if owner not in owners:
            owners.append(owner)

    # Only one owner means that player owns the whole map
    if len(owners) == 1:
        return owners[0]

    return None

# Reset all territories to their original starting state
def reset_game():

    global territories

    territories = copy.deepcopy(starting_territories)

    print("\nThe game has been reset.")

# Temporary choice used to test the game
def choose_test_reinforcement(player_name):

    player_territories = get_player_territories(player_name)

    # Find a territory next to an enemy
    for territory_name in player_territories:

        neighbours = territories[territory_name]["neighbours"]

        for neighbour_name in neighbours:

            neighbour_owner = territories[neighbour_name]["owner"]

            if neighbour_owner != player_name:
                return territory_name

    # Use the first owned territory if there is no enemy border
    return player_territories[0]    

# Temporary attack choice used to test the game
def choose_test_attack(player_name, reinforcement_territory):

    neighbours = territories[reinforcement_territory]["neighbours"]

    # Find the first neighbouring enemy territory
    for neighbour_name in neighbours:

        neighbour_owner = territories[neighbour_name]["owner"]

        if neighbour_owner != player_name:

            return (
                reinforcement_territory,
                neighbour_name
            )

    # None means do not attack
    return None

# Play one complete turn for an AI agent
# Play one complete turn for an AI agent
def play_agent_turn(
    player_name,
    agent_name,
    max_attack_rounds=5
):

    print("\n==============================")
    print(player_name, "-", agent_name, "turn")
    print("==============================")


    # --------------------------------
    # Reinforcement decision
    # --------------------------------

    decision_start_time = time.perf_counter()

    if agent_name == "Random Agent":

        reinforcement_territory = choose_random_reinforcement(
            player_name,
            territories
        )

    elif agent_name == "Rule-Based Agent":

        reinforcement_territory = choose_rule_reinforcement(
            player_name,
            territories
        )

    elif agent_name == "Heuristic Agent":

        reinforcement_territory = choose_heuristic_reinforcement(
            player_name,
            territories
        )

    elif agent_name == "Monte Carlo Agent":

        reinforcement_territory = choose_monte_carlo_reinforcement(
            player_name,
            territories
        )

    else:

        print("Unknown agent:", agent_name)
        return


    decision_end_time = time.perf_counter()

    reinforcement_decision_time = (
        decision_end_time - decision_start_time
    )

    game_metrics[player_name]["decisions_made"] += 1

    game_metrics[player_name]["decision_time_seconds"] += (
        reinforcement_decision_time
    )


    # --------------------------------
    # Add reinforcement armies
    # --------------------------------

    reinforcements = calculate_reinforcements(
        player_name
    )

    print(
        player_name,
        "receives",
        reinforcements,
        "reinforcement armies."
    )

    print(
        agent_name,
        "reinforces territory",
        reinforcement_territory
    )

    reinforce_territory(
        player_name,
        reinforcement_territory,
        reinforcements
    )


    # --------------------------------
    # Attack phase
    # --------------------------------

    for attack_round in range(
        1,
        max_attack_rounds + 1
    ):

        valid_attacks = get_valid_attacks(
            player_name
        )

        if len(valid_attacks) == 0:

            print(
                player_name,
                "has no valid attacks."
            )

            break


        # Start measuring attack decision time
        decision_start_time = time.perf_counter()


        if agent_name == "Random Agent":

            attack_choice = choose_random_attack(
                valid_attacks
            )


        elif agent_name == "Rule-Based Agent":

            attack_choice = choose_rule_attack(
                valid_attacks,
                territories
            )


        elif agent_name == "Heuristic Agent":

            attack_choice = choose_heuristic_attack(
                valid_attacks,
                territories
            )


        elif agent_name == "Monte Carlo Agent":

            simulations_per_attack = 100

            attack_choice = choose_monte_carlo_attack(
                valid_attacks,
                territories,
                simulations=simulations_per_attack,
                max_rounds=max_attack_rounds
            )

            # Each valid attack is simulated 100 times
            simulations_this_decision = (
                len(valid_attacks)
                * simulations_per_attack
            )

            game_metrics[player_name]["simulations_run"] += (
                simulations_this_decision
            )


        else:

            print("Unknown agent:", agent_name)
            return


        # Stop measuring decision time
        decision_end_time = time.perf_counter()

        attack_decision_time = (
            decision_end_time - decision_start_time
        )

        game_metrics[player_name]["decisions_made"] += 1

        game_metrics[player_name]["decision_time_seconds"] += (
            attack_decision_time
        )


        print("\nAttack round:", attack_round)

        print(
            agent_name,
            "chooses:",
            attack_choice
        )


        if attack_choice is None:

            print(
                agent_name,
                "decided to stop attacking."
            )

            break


        attacking_territory = attack_choice[0]
        defending_territory = attack_choice[1]


        attack_territory(
            attacking_territory,
            defending_territory
        )


        winner = check_winner()

        if winner is not None:
            break

# Run a complete game between two agents
# Run one complete game between two agents
def play_game(
    max_turns=100,
    player_1_agent="Random Agent",
    player_2_agent="Rule-Based Agent",
    random_seed=None
):
    # Use a fixed seed when one is provided
    if random_seed is not None:
        random.seed(random_seed)

    # Reset only once, before the game begins
    reset_game()
    reset_game_metrics()

    print("\nThe game has started.")
    show_game_state()

    # Player 1 starts first
    current_player_index = 0

    # Start the turn loop
    for turn_number in range(1, max_turns + 1):

        current_player = players[current_player_index]

        print("\n--------------------------------")
        print("Turn number:", turn_number)
        print("Current player:", current_player)
        print("--------------------------------")

        # Select the agent controlling the player
        if current_player == "Player 1":
            agent_name = player_1_agent

        else:
            agent_name = player_2_agent

        # Run the complete turn
        play_agent_turn(
            current_player,
            agent_name,
            max_attack_rounds=5
        )

        # Check for a winner
        winner = check_winner()

        if winner is not None:

            print("\n==============================")
            print("Game finished")
            print("Winner:", winner)
            print("Turns played:", turn_number)
            print("==============================")

            show_game_state()

            return (
                winner,
                turn_number,
                copy.deepcopy(game_metrics)
            )

        # Move to the other player
        if current_player_index == 0:
            current_player_index = 1

        else:
            current_player_index = 0

    # No winner after reaching the limit
    print("\nThe game reached the maximum turn limit.")
    print("No winner was found.")

    show_game_state()

    return (
    None,
    max_turns,
    copy.deepcopy(game_metrics)
    )

# Reset performance metrics before a new game
def reset_game_metrics():

    global game_metrics

    game_metrics = {
        "Player 1": {
            "attacks_made": 0,
            "successful_attacks": 0,
            "armies_lost": 0,
            "territories_captured": 0,
            "decisions_made": 0,
            "decision_time_seconds": 0.0,
            "simulations_run": 0
        },

        "Player 2": {
            "attacks_made": 0,
            "successful_attacks": 0,
            "armies_lost": 0,
            "territories_captured": 0,
            "decisions_made": 0,
            "decision_time_seconds": 0.0,
            "simulations_run": 0
        }
    }

# Display performance metrics for both players
def show_game_metrics():

    print("\n==============================")
    print("Game Performance Metrics")
    print("==============================")

    for player_name, metrics in game_metrics.items():

        attacks_made = metrics["attacks_made"]
        successful_attacks = metrics["successful_attacks"]
        armies_lost = metrics["armies_lost"]
        territories_captured = metrics["territories_captured"]

        decisions_made = metrics["decisions_made"]

        decision_time_seconds = metrics[
            "decision_time_seconds"
        ]

        simulations_run = metrics["simulations_run"]

        # Avoid division by zero
        if attacks_made > 0:
            success_rate = (
                successful_attacks / attacks_made
            ) * 100
        else:
            success_rate = 0

        print("\n", player_name)
        print("Attacks made:", attacks_made)
        print("Successful attacks:", successful_attacks)
        print(
            "Attack success rate:",
            round(success_rate, 2),
            "%"
        )
        print("Armies lost:", armies_lost)
        print(
            "Territories captured:",
            territories_captured
        )

        if decisions_made > 0:

            average_decision_time = (
                decision_time_seconds / decisions_made
            )

        else:

            average_decision_time = 0


        print("Decisions made:", decisions_made)

        print(
            "Total decision time:",
            round(decision_time_seconds, 6),
            "seconds"
        )

        print(
            "Average decision time:",
            round(average_decision_time, 6),
            "seconds"
        )

        print(
            "Monte Carlo simulations:",
            simulations_run
        )

# Display the current game state
def show_game_state():

    print("\nCurrent Game State")
    print("------------------")

    for territory_name, territory_data in territories.items():

        owner = territory_data["owner"]
        armies = territory_data["armies"]
        neighbours = territory_data["neighbours"]

        print(
            territory_name,
            "| Owner:", owner,
            "| Armies:", armies,
            "| Neighbours:", neighbours
        )


if __name__ == "__main__":

    winner, turns_played, metrics = play_game(
        max_turns=100,
        player_1_agent="Monte Carlo Agent",
        player_2_agent="Heuristic Agent"
    )

    print("\nFinal result")
    print("Winner:", winner)
    print("Turns played:", turns_played)

    show_game_metrics()