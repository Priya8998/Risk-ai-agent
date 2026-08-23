# Testing and Validation

## Final Automated Test Run

Date: 23 August 2026

The simplified RISK simulator was validated using Python's built-in `unittest` framework.

Command used:

```powershell
python -m unittest discover -s tests -v

Ran 12 tests in 0.009s

OK

## Reproducibility Validation

A separate reproducibility check was performed using the same game configuration and random seed twice.

Test configuration:

- Player 1: Rule-Based Agent
- Player 2: Monte Carlo Agent
- Random seed: 12345
- Maximum turns: 100

Results:

First run:
- Winner: Player 2
- Turns: 36

Second run:
- Winner: Player 2
- Turns: 36

Result:

Reproducibility check: PASSED

Decision-time measurements were excluded from the comparison because execution time can vary slightly depending on computer workload.

This test demonstrates that the simulator produces reproducible non-timing game outcomes when the same random seed, code and configuration are used.