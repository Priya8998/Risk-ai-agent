# Choose a border territory using a threat score
def choose_heuristic_reinforcement(
    player_name,
    territories
):

    owned_territories = []

    # Find all territories owned by the player
    for territory_name, territory_data in territories.items():

        if territory_data["owner"] == player_name:
            owned_territories.append(territory_name)

    # Begin with the first owned territory
    best_territory = owned_territories[0]
    best_score = -999

    # Calculate a reinforcement score for each territory
    for territory_name in owned_territories:

        territory_data = territories[territory_name]

        own_armies = territory_data["armies"]

        enemy_count = 0
        total_enemy_armies = 0

        # Check neighbouring territories
        for neighbour_name in territory_data["neighbours"]:

            neighbour_data = territories[neighbour_name]

            if neighbour_data["owner"] != player_name:

                enemy_count += 1
                total_enemy_armies += neighbour_data["armies"]

        # Ignore territories that do not border an enemy
        if enemy_count == 0:
            continue

        # Higher score means the territory needs more support
        score = (
            total_enemy_armies
            - own_armies
            + enemy_count * 2
        )

        if score > best_score:

            best_score = score
            best_territory = territory_name

    return best_territory


# Choose an attack using a heuristic score
def choose_heuristic_attack(
    valid_attacks,
    territories
):

    best_attack = None
    best_score = 0

    # Score every valid attack
    for attack in valid_attacks:

        attacking_territory = attack[0]
        defending_territory = attack[1]

        attacking_armies = territories[
            attacking_territory
        ]["armies"]

        defending_armies = territories[
            defending_territory
        ]["armies"]

        # Avoid attacking with equal or fewer armies
        if attacking_armies <= defending_armies:
            continue

        # Calculate the army advantage
        army_advantage = (
            attacking_armies - defending_armies
        )

        # Connected territories may be strategically useful
        connection_score = len(
            territories[defending_territory]["neighbours"]
        )

        # Give a bonus when the enemy has only one army
        capture_bonus = 0

        if defending_armies == 1:
            capture_bonus = 3

        # Final heuristic score
        score = (
            army_advantage * 3
            + connection_score
            + capture_bonus
        )

        if score > best_score:

            best_score = score
            best_attack = attack

    return best_attack