# Simplified RISK AI Agent Comparison

## Project Overview

This project implements a simplified version of the RISK board game in Python.

The purpose of the project is to build and compare several AI agents in a stochastic strategy-game environment. The agents make reinforcement and attack decisions while the game engine controls the rules, dice rolls, territory ownership and winning condition.

The project currently contains four agents:

- Random Agent
- Rule-Based Agent
- Heuristic Agent
- Monte Carlo Agent

Monte Carlo Tree Search may be added later as an extension.

---

## Research Aim

The main aim is to investigate whether more advanced AI decision-making methods perform better than simpler methods in a simplified RISK environment.

The project also examines the computational cost of each agent.

---

## Research Question

> Does increasing the intelligence and computational complexity of an AI agent improve its performance in a simplified RISK game?

---

## Simplified Game Environment

The simulator uses:

- Two players
- Six territories
- Territory ownership
- Army reinforcement
- Neighbour-based attacks
- Dice-based combat
- Territory capture
- Alternating player turns
- Maximum turn limit
- Winning condition

The project intentionally uses a smaller map so the game logic and AI behaviour can be developed, tested and evaluated clearly.

---

## Game Map

The simplified map contains six territories:

```text
          A
         / \
        B---C
        |   |
        D---E
         \ /
          F
```

Player 1 initially owns:

```text
A, B and C
```

Player 2 initially owns:

```text
D, E and F
```

Each territory begins with three armies.

The main starting attack connections between the players are:

```text
B → D
C → E
D → B
E → C
```

---

## Simplified Reinforcement Rule

The reinforcement calculation is:

```text
Number of territories owned // 3
```

The minimum reinforcement is one army.

The official RISK minimum of three armies was reduced because this project uses only six territories. Using three reinforcements on the small map caused long stalemates and excessive army growth.

---

## Dice Combat Rules

The combat system follows these simplified RISK rules:

- The attacker must leave at least one army behind.
- The attacker can roll up to three dice.
- The defender can roll up to two dice.
- Dice are sorted from highest to lowest.
- The highest attacker die is compared with the highest defender die.
- The second-highest dice are compared when available.
- The lower result loses one army.
- The defender wins when the dice are equal.
- A territory is captured when its defending armies reach zero.
- One attacking army moves into the captured territory.

---

## Project Architecture

```text
Experiment or Tournament Runner
              |
              v
        Agent Selection
              |
              v
-------------------------------------------------
| Random | Rule-Based | Heuristic | Monte Carlo |
-------------------------------------------------
              |
              v
          RISK Game Engine
              |
              v
-------------------------------------------------
| Reinforcement                                  |
| Attack Validation                              |
| Dice Combat                                    |
| Army Updates                                   |
| Territory Capture                              |
| Winner Detection                               |
-------------------------------------------------
              |
              v
        Performance Metrics
              |
              v
          CSV Result Files
              |
              v
 Statistical Analysis and Visualisations
```

---

## Separation Between Agents and Game Engine

The AI agents choose actions, but they do not directly change the game.

The process is:

```text
Agent observes the current game state
              |
              v
Agent chooses reinforcement or attack
              |
              v
Game engine validates the decision
              |
              v
Game engine rolls dice and updates the state
              |
              v
Agent observes the new state on its next decision
```

This separation ensures that every agent follows the same rules.

---

## AI Agents

### Random Agent

The Random Agent is the simplest baseline.

It:

- Randomly selects one of its territories for reinforcement.
- Randomly selects one of the valid attacks.
- Can randomly decide not to attack.
- Does not consider army strength or future outcomes.

The Random Agent is useful because it provides a basic performance level against which the other agents can be compared.

---

### Rule-Based Agent

The Rule-Based Agent follows fixed decision rules.

It:

- Identifies territories that border an enemy.
- Reinforces its strongest border territory.
- Attacks only when the attacking territory has more armies than the defender.
- Prefers to attack the weakest available enemy territory.
- Stops when no suitable attack is available.

The Rule-Based Agent is more purposeful than the Random Agent but does not calculate scores or simulate future outcomes.

---

### Heuristic Agent

The Heuristic Agent assigns scores to possible reinforcement and attack decisions.

Its reinforcement score considers:

- The territory's current armies.
- The number of neighbouring enemies.
- The total armies in neighbouring enemy territories.
- The level of threat to the territory.

Its attack score considers:

- Army advantage.
- Defender army strength.
- Territory connectivity.
- Opportunity to capture a weak territory.

The agent chooses the option with the highest heuristic score.

A heuristic is a practical estimate used to make a good decision without examining every possible future state.

---

### Monte Carlo Agent

The Monte Carlo Agent uses repeated random simulations.

For each valid attack, it:

1. Reads the current attacking and defending armies.
2. Simulates the battle many times.
3. Estimates the probability of capturing the territory.
4. Estimates the remaining attacker and defender armies.
5. calculates a score for the attack.
6. Selects the attack with the best simulated outcome.
7. Stops when the estimated capture probability is too low.

The current version uses 100 simulations for every valid attack decision.

The Monte Carlo Agent usually requires more computation than the other agents.

---

## Performance Metrics

The simulator records the following metrics for every player:

- Attacks made
- Successful attacks
- Attack success rate
- Armies lost
- Territories captured
- Decisions made
- Total decision time
- Average decision time
- Monte Carlo simulations performed

The experiment and tournament files also record:

- Wins
- Losses
- Draws
- Win rate
- Draw rate
- Turns played
- Average game length
- Starting-player position
- Random seed
- 95% confidence interval

---

## Meaning of a Successful Attack

A successful attack means that the defender lost at least one army during a battle round.

This is different from territory capture.

For example:

```text
Defender loses one army
Territory is not captured
```

This still counts as a successful attack.

---

## Territory Capture Metric

The territory-capture metric counts every capture event.

A territory can be:

```text
Captured
Lost
Captured again
```

Therefore, the number of territories captured during a game can be greater than the six territories on the map.

---

## Reproducibility

The final evaluation uses fixed random seeds.

A random seed controls:

- Dice results
- Random Agent decisions
- Monte Carlo simulation outcomes

Using the same:

- Source code
- Agent configuration
- Random seed
- Maximum turn limit

should reproduce the same:

- Winner
- Number of turns
- Attacks
- Armies lost
- Territory captures
- Simulation count

Decision-time values may vary slightly because they depend on computer workload.

---

## Fair Experimental Design

The agents alternate between Player 1 and Player 2.

For example:

```text
Game 1:
Player 1 = Random Agent
Player 2 = Heuristic Agent

Game 2:
Player 1 = Heuristic Agent
Player 2 = Random Agent
```

This reduces the effect of first-player advantage.

Every agent plays against every other agent in the tournament.

With four agents, the six pairings are:

```text
Random vs Rule-Based
Random vs Heuristic
Random vs Monte Carlo
Rule-Based vs Heuristic
Rule-Based vs Monte Carlo
Heuristic vs Monte Carlo
```

---

## Project Structure

```text
risk_ai_project/
|
|-- risk_game.py
|-- experiments.py
|-- analyse_results.py
|-- tournament.py
|-- visualise_tournament.py
|-- final_evaluation.py
|-- final_analysis.py
|-- requirements.txt
|-- README.md
|
|-- agents/
|   |-- __init__.py
|   |-- random_agent.py
|   |-- rule_based_agent.py
|   |-- heuristic_agent.py
|   |-- monte_carlo_agent.py
|
|-- tests/
|   |-- test_risk_game.py
|
|-- results/
|   |-- all_agents_tournament.csv
|   |-- final_reproducible_tournament.csv
|   |-- final_agent_summary.csv
|   |-- final_head_to_head_summary.csv
|   |-- final_starting_position_summary.csv
|   |-- final_evaluation_config.txt
|   |-- reproducibility_report.txt
|   |
|   |-- final_graphs/
|       |-- win_rate_confidence_intervals.png
|       |-- draw_rate.png
|       |-- attack_success_rate.png
|       |-- decision_time.png
|       |-- simulations_per_game.png
|       |-- starting_position_comparison.png
```

Some result files are created only after the corresponding scripts are executed.

---

## Installation

Python must be installed before running the project.

Install the required external package with:

```powershell
python -m pip install -r requirements.txt
```

The current external requirement is:

```text
matplotlib
```

Other modules used by the project are part of the Python standard library.

---

## Run One Game

Run:

```powershell
python risk_game.py
```

The agents for the manual game are selected at the bottom of `risk_game.py`.

Example:

```python
winner, turns_played, metrics = play_game(
    max_turns=100,
    player_1_agent="Monte Carlo Agent",
    player_2_agent="Heuristic Agent",
    random_seed=12345
)
```

---

## Run One Agent Comparison

Open `experiments.py` and choose the two agents:

```python
agent_a = "Monte Carlo Agent"
agent_b = "Heuristic Agent"
```

Then run:

```powershell
python experiments.py
```

The results are saved as a CSV file inside the `results` folder.

---

## Analyse One Agent Comparison

Select the correct CSV filename inside `analyse_results.py`.

Then run:

```powershell
python analyse_results.py
```

This displays performance statistics for the two selected agents.

---

## Run the Development Tournament

Run:

```powershell
python tournament.py
```

This runs every agent against every other agent and saves the raw results to:

```text
results/all_agents_tournament.csv
```

---

## Create Development Graphs

Run:

```powershell
python visualise_tournament.py
```

This creates summary results and graphs from the development tournament.

---

## Run the Final Reproducible Evaluation

Run:

```powershell
python final_evaluation.py
```

The final evaluation:

- Runs every agent pairing.
- Alternates player positions.
- Uses a unique fixed seed for every game.
- Records performance metrics.
- Records computational metrics.
- Saves the raw results.

The main output file is:

```text
results/final_reproducible_tournament.csv
```

---

## Run the Final Statistical Analysis

After the final evaluation finishes, run:

```powershell
python final_analysis.py
```

This creates:

- Final agent summary
- Head-to-head comparison
- Starting-position analysis
- Reproducibility report
- Final dissertation graphs
- 95% confidence intervals

---

## Run Automated Tests

Run this command from the main project folder:

```powershell
python -m unittest discover -s tests -v
```

The tests validate:

- Starting territory ownership
- Valid attacks
- Reinforcement calculation
- Valid reinforcement
- Invalid reinforcement
- Defender winning equal dice
- Territory capture
- Invalid attacks
- Winner detection
- Game reset
- Metrics reset
- Random-seed reproducibility

---

## Current Limitations

This project is a simplified experimental implementation of RISK.

Current limitations include:

- Only six territories.
- Only two players.
- No continent bonuses.
- No territory cards.
- No card trading.
- No fortification phase.
- Maximum of five attack decisions per turn.
- Simplified reinforcement rule.
- Simplified agent strategies.
- Monte Carlo simulations focus on local battle outcomes rather than complete future games.
- No human-player interface.
- No Monte Carlo Tree Search agent yet.

The experimental findings apply to this implemented environment and should not automatically be generalised to the complete commercial RISK game.

---

## Future Work

Possible future extensions include:

- Monte Carlo Tree Search
- Full 42-territory map
- Three or more players
- Continents and continent bonuses
- Territory cards
- Card trading
- Fortification decisions
- Reinforcement learning
- Neural-network-based agents
- Human-versus-agent evaluation
- Web-based graphical interface
- More detailed reward functions
- Larger sensitivity experiments

---

## Dissertation Use

The project provides evidence for the dissertation through:

- Python source code
- Automated tests
- Raw experiment results
- Reproducible random seeds
- Performance metrics
- Statistical summaries
- Confidence intervals
- Head-to-head comparisons
- Computational-cost measurements
- Graphs and visualisations