import random


# Choose a border territory to reinforce
def choose_monte_carlo_reinforcement(
    player_name,
    territories
):

    border_territories = []

    # Find territories next to an enemy
    for territory_name, territory_data in territories.items():

        if territory_data["owner"] == player_name:

            for neighbour_name in territory_data["neighbours"]:

                neighbour_owner = territories[
                    neighbour_name
                ]["owner"]

                if neighbour_owner != player_name:

                    border_territories.append(
                        territory_name
                    )

                    break

    # Use the first owned territory if no border exists
    if len(border_territories) == 0:

        for territory_name, territory_data in territories.items():

            if territory_data["owner"] == player_name:
                return territory_name

    # Start with the first border territory
    best_territory = border_territories[0]
    best_score = -999

    # Find the border with the best attack opportunity
    for territory_name in border_territories:

        own_armies = territories[
            territory_name
        ]["armies"]

        weakest_enemy_armies = 999

        for neighbour_name in territories[
            territory_name
        ]["neighbours"]:

            neighbour_data = territories[neighbour_name]

            if neighbour_data["owner"] != player_name:

                enemy_armies = neighbour_data["armies"]

                if enemy_armies < weakest_enemy_armies:
                    weakest_enemy_armies = enemy_armies

        # Higher score means a better attacking position
        score = own_armies - weakest_enemy_armies

        if score > best_score:

            best_score = score
            best_territory = territory_name

    return best_territory


# Simulate one possible attack
def simulate_attack(
    attacking_armies,
    defending_armies,
    max_rounds=5
):

    simulated_attacker = attacking_armies
    simulated_defender = defending_armies

    # Simulate several battle rounds
    for battle_round in range(max_rounds):

        # Stop if the attacker cannot continue
        if simulated_attacker <= 1:
            break

        # Stop if the defender has been defeated
        if simulated_defender <= 0:
            break

        attacker_dice_count = min(
            3,
            simulated_attacker - 1
        )

        defender_dice_count = min(
            2,
            simulated_defender
        )

        attacker_dice = []
        defender_dice = []

        # Roll attacker dice
        for dice in range(attacker_dice_count):

            attacker_dice.append(
                random.randint(1, 6)
            )

        # Roll defender dice
        for dice in range(defender_dice_count):

            defender_dice.append(
                random.randint(1, 6)
            )

        # Highest dice must be compared first
        attacker_dice.sort(reverse=True)
        defender_dice.sort(reverse=True)

        comparisons = min(
            len(attacker_dice),
            len(defender_dice)
        )

        # Compare dice
        for position in range(comparisons):

            attacker_result = attacker_dice[position]
            defender_result = defender_dice[position]

            if attacker_result > defender_result:
                simulated_defender -= 1

            else:
                simulated_attacker -= 1

    territory_captured = simulated_defender <= 0

    return (
        territory_captured,
        simulated_attacker,
        simulated_defender
    )


# Use repeated simulations to choose an attack
def choose_monte_carlo_attack(
    valid_attacks,
    territories,
    simulations=100,
    max_rounds=5
):

    if len(valid_attacks) == 0:
        return None

    best_attack = None
    best_score = -999
    best_capture_rate = 0

    # Test every valid attack
    for attack in valid_attacks:

        attacking_territory = attack[0]
        defending_territory = attack[1]

        attacking_armies = territories[
            attacking_territory
        ]["armies"]

        defending_armies = territories[
            defending_territory
        ]["armies"]

        captures = 0
        total_army_difference = 0

        # Simulate this attack many times
        for simulation_number in range(simulations):

            (
                captured,
                remaining_attacker,
                remaining_defender
            ) = simulate_attack(
                attacking_armies,
                defending_armies,
                max_rounds
            )

            if captured:
                captures += 1

            army_difference = (
                remaining_attacker
                - remaining_defender
            )

            total_army_difference += army_difference

        capture_rate = captures / simulations

        average_army_difference = (
            total_army_difference / simulations
        )

        # Capturing territory is the most important result
        score = (
            capture_rate * 100
            + average_army_difference
        )

        if score > best_score:

            best_score = score
            best_attack = attack
            best_capture_rate = capture_rate

    # Avoid attacks with a very low estimated chance
    if best_capture_rate < 0.30:
        return None

    return best_attack