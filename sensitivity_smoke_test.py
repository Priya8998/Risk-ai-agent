from risk_game import play_game

import io
from contextlib import redirect_stdout


def test_simulation_setting(simulations):

    with redirect_stdout(io.StringIO()):

        winner, turns, metrics = play_game(
            max_turns=100,
            player_1_agent="Monte Carlo Agent",
            player_2_agent="Rule-Based Agent",
            random_seed=12345,
            monte_carlo_simulations=simulations
        )

    print("Simulations per attack:", simulations)
    print("Winner:", winner)
    print("Turns:", turns)
    print(
        "Total Monte Carlo simulations:",
        metrics["Player 1"]["simulations_run"]
    )
    print()

test_simulation_setting(10)
test_simulation_setting(250)