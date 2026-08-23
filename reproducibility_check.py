from risk_game import play_game

import io
from contextlib import redirect_stdout


def run_same_game(seed):

    # Hide normal game output
    with redirect_stdout(io.StringIO()):

        winner, turns, metrics = play_game(
            max_turns=100,
            player_1_agent="Rule-Based Agent",
            player_2_agent="Monte Carlo Agent",
            random_seed=seed
        )

    # Decision time can change slightly between runs,
    # so remove it before comparing results.
    for player_name in metrics:
        metrics[player_name].pop(
            "decision_time_seconds",
            None
        )

    return winner, turns, metrics


seed = 12345

first_run = run_same_game(seed)
second_run = run_same_game(seed)


print("Seed used:", seed)

print()
print("First run")
print("Winner:", first_run[0])
print("Turns:", first_run[1])

print()
print("Second run")
print("Winner:", second_run[0])
print("Turns:", second_run[1])

print()

if first_run == second_run:
    print("Reproducibility check: PASSED")
else:
    print("Reproducibility check: FAILED")