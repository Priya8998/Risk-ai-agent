import random


# Choose one owned territory randomly for reinforcement
def choose_random_reinforcement(player_name, territories):

    owned_territories = []

    for territory_name, territory_data in territories.items():

        if territory_data["owner"] == player_name:
            owned_territories.append(territory_name)

    chosen_territory = random.choice(owned_territories)

    return chosen_territory


# Choose one valid attack randomly
def choose_random_attack(valid_attacks):

    attack_options = valid_attacks.copy()

    # None means the agent chooses not to attack
    attack_options.append(None)

    chosen_attack = random.choice(attack_options)

    return chosen_attack