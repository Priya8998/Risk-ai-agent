# Choose the strongest border territory for reinforcement
def choose_rule_reinforcement(player_name, territories):

    border_territories = []

    # Find territories that are next to an enemy
    for territory_name, territory_data in territories.items():

        if territory_data["owner"] == player_name:

            for neighbour_name in territory_data["neighbours"]:

                neighbour_owner = territories[neighbour_name]["owner"]

                if neighbour_owner != player_name:
                    border_territories.append(territory_name)
                    break

    # Start with the first border territory
    strongest_territory = border_territories[0]

    # Find the border territory with the most armies
    for territory_name in border_territories:

        territory_armies = territories[territory_name]["armies"]
        strongest_armies = territories[strongest_territory]["armies"]

        if territory_armies > strongest_armies:
            strongest_territory = territory_name

    return strongest_territory


# Choose the best available attack
def choose_rule_attack(valid_attacks, territories):

    possible_attacks = []

    # Keep attacks where the attacker is stronger
    for attack in valid_attacks:

        attacking_territory = attack[0]
        defending_territory = attack[1]

        attacking_armies = territories[attacking_territory]["armies"]
        defending_armies = territories[defending_territory]["armies"]

        if attacking_armies > defending_armies:
            possible_attacks.append(attack)

    # Stop when no suitable attack exists
    if len(possible_attacks) == 0:
        return None

    best_attack = possible_attacks[0]

    # Prefer the weakest enemy territory
    for attack in possible_attacks:

        defending_territory = attack[1]
        best_defending_territory = best_attack[1]

        defending_armies = territories[defending_territory]["armies"]
        best_defending_armies = territories[best_defending_territory]["armies"]

        if defending_armies < best_defending_armies:
            best_attack = attack

    return best_attack