# Dissertation Methodology

## 1. Research Design

This project uses a quantitative experimental research design to compare the performance of different artificial intelligence agents in a simplified version of the RISK strategy board game.

The study implements a controlled Python simulation in which multiple AI agents play repeated games under the same rules and starting conditions.

The agents currently evaluated are:

- Random Agent
- Rule-Based Agent
- Heuristic Agent
- Monte Carlo Agent

The independent variable is the decision-making method used by each agent.

The dependent variables are the performance and computational metrics produced during the games, including:

- Win rate
- Draw rate
- Game length
- Attack success rate
- Armies lost
- Territories captured
- Decision time
- Number of simulations performed

The experiment investigates whether more advanced decision-making methods improve game performance and whether any improvement justifies the additional computational cost.

---

## 2. Research Aim

The aim of the project is to design, implement and evaluate AI agents with different levels of decision-making complexity in a stochastic strategy-game environment.

The project compares simple baseline behaviour with rule-based, heuristic and simulation-based decision-making.

---

## 3. Research Question

The main research question is:

> Does increasing the intelligence and computational complexity of an AI agent improve its performance in a simplified RISK game?

The project also considers the following supporting questions:

1. Does the Rule-Based Agent perform better than the Random Agent?
2. Does heuristic scoring improve performance compared with fixed rules?
3. Does the Monte Carlo Agent achieve a higher win rate than simpler agents?
4. What computational cost is introduced by Monte Carlo simulation?
5. Does playing first provide a measurable advantage?
6. How frequently do games reach the maximum turn limit?
7. Are the experimental results reproducible when fixed random seeds are used?

---

## 4. Development Approach

The project follows an incremental development approach.

The simulator and agents were developed in the following order:

```text
Define simplified game rules
            |
            v
Create territory and map structure
            |
            v
Implement reinforcement
            |
            v
Implement attack validation
            |
            v
Implement dice combat
            |
            v
Implement territory capture
            |
            v
Implement winner detection
            |
            v
Create automatic player turns
            |
            v
Develop Random Agent
            |
            v
Develop Rule-Based Agent
            |
            v
Develop Heuristic Agent
            |
            v
Develop Monte Carlo Agent
            |
            v
Add performance metrics
            |
            v
Add reproducible experiments
            |
            v
Run final high-volume evaluation
            |
            v
Perform statistical analysis
```

Each component was tested before the next component was added.

This approach reduced implementation complexity and allowed errors in the game rules or agent behaviour to be identified early.

---

## 5. Experimental Environment

The experiment uses a simplified implementation of RISK written in Python.

The environment contains:

- Two players
- Six territories
- Three starting territories per player
- Three starting armies per territory
- Reinforcement decisions
- Attack decisions
- Dice-based combat
- Territory capture
- Alternating turns
- A maximum turn limit
- A winning condition

The simplified environment was selected because the complete commercial RISK game includes 42 territories, continent bonuses, cards, card trading, fortification and multiple players.

Implementing the complete game would significantly increase the state space and computational cost.

The smaller environment allows the decision-making behaviour of the agents to be analysed clearly while retaining important characteristics of RISK:

- Strategic territory control
- Army allocation
- Neighbour-based attacks
- Random dice outcomes
- Competition between players
- Sequential decision-making

---

## 6. Simplified Game Map

The experimental map contains six territories:

```text
          A
         / \
        B---C
        |   |
        D---E
         \ /
          F
```

Player 1 begins with:

```text
A, B and C
```

Player 2 begins with:

```text
D, E and F
```

Each territory begins with three armies.

The initial enemy-border connections are:

```text
B and D
C and E
```

This creates a balanced starting structure in which each player controls the same number of territories and armies.

---

## 7. Game-State Representation

The game state is represented using a Python dictionary.

Each territory stores:

- Territory name
- Current owner
- Number of armies
- Neighbouring territories

Example:

```python
"A": {
    "owner": "Player 1",
    "armies": 3,
    "neighbours": ["B", "C"]
}
```

This structure allows the simulator to determine:

- Which territories belong to each player
- Which attacks are valid
- Which territories border an enemy
- How many armies are available
- Whether a player has captured the entire map

---

## 8. Reinforcement Method

At the start of each turn, the current player receives reinforcement armies.

The reinforcement calculation is:

```text
Number of owned territories // 3
```

The minimum reinforcement is one army.

For example:

```text
Three territories // 3 = one reinforcement army
```

The official RISK minimum of three reinforcement armies was reduced because the experimental map contains only six territories.

During early testing, giving three reinforcement armies every turn produced excessive army growth and long stalemates.

The smaller reinforcement value was therefore selected to better match the reduced map size.

---

## 9. Attack Rules

An attack is valid only when:

- The attacking territory exists.
- The defending territory exists.
- The territories are neighbours.
- The territories have different owners.
- The attacking territory contains more than one army.

At least one army must remain in the attacking territory.

The game engine generates all valid attacks before an agent makes its decision.

This prevents agents from selecting actions that violate the game rules.

---

## 10. Dice Combat

The attacker can roll up to three dice.

The number of attacker dice is calculated as:

```text
Minimum of:
- Three dice
- Attacking armies minus one
```

The defender can roll up to two dice.

The number of defender dice is calculated as:

```text
Minimum of:
- Two dice
- Number of defending armies
```

The dice are sorted from highest to lowest.

The highest attacker die is compared with the highest defender die.

When both sides have another die available, the second-highest dice are also compared.

The side with the lower die loses one army.

When the dice are equal, the defender wins and the attacker loses one army.

This preserves an important defensive advantage from the original RISK combat system.

---

## 11. Territory Capture

A territory is captured when its defending armies reach zero.

When a capture occurs:

1. The territory owner changes to the attacking player.
2. One army is removed from the attacking territory.
3. That army is placed in the captured territory.
4. The territory-capture metric is increased.
5. The valid attack list is recalculated.

A territory may be captured, lost and captured again during the same game.

Therefore, the number of territory-capture events may be greater than the total number of territories on the map.

---

## 12. Turn Structure

A complete agent turn contains the following stages:

```text
Start turn
    |
    v
Choose reinforcement territory
    |
    v
Calculate reinforcement amount
    |
    v
Add reinforcement armies
    |
    v
Generate valid attacks
    |
    v
Choose an attack or stop
    |
    v
Execute dice combat
    |
    v
Update armies and ownership
    |
    v
Check for winner
    |
    v
Recalculate valid attacks
    |
    v
Continue attacking or end turn
```

Each agent can make a maximum of five attack decisions in one turn.

The attack options are recalculated after every battle so that the agent can react to territory captures and army losses.

---

## 13. Winning and Draw Conditions

A player wins when they own every territory on the map.

The game engine checks the owners of all six territories after each attack.

A game is recorded as a draw when no player wins before the maximum turn limit.

The final evaluation uses:

```text
Maximum turns per game: 100
```

The turn limit prevents games from continuing indefinitely when both agents become defensive or repeatedly fail to capture territories.

---

## 14. Agent Implementation

All agents use the same game engine.

The agents receive information about the current state and return a selected action.

Agents cannot directly:

- Change territory ownership
- Add armies
- Remove armies
- Generate dice results
- Declare a winner

These responsibilities remain inside the game engine.

This separation ensures fairness because every agent follows the same rules.

---

## 15. Random Agent

The Random Agent is used as the baseline.

For reinforcement, it randomly selects one of its owned territories.

For attacking, it randomly selects:

- One valid attack
- Or the option to stop attacking

The Random Agent does not consider:

- Army advantage
- Territory value
- Enemy strength
- Capture probability
- Future game states

Its purpose is to provide a minimum performance baseline.

---

## 16. Rule-Based Agent

The Rule-Based Agent follows fixed strategic rules.

For reinforcement, it:

1. Identifies territories next to an enemy.
2. Selects the border territory with the largest number of armies.
3. Adds reinforcement armies to that territory.

For attacking, it:

1. Examines all valid attacks.
2. Removes attacks where the attacker is not stronger than the defender.
3. Selects the attack against the weakest suitable enemy.
4. Stops when no suitable attack exists.

The Rule-Based Agent is more purposeful than the Random Agent but does not score all actions or simulate future outcomes.

---

## 17. Heuristic Agent

The Heuristic Agent calculates scores for possible decisions.

### Reinforcement scoring

The reinforcement score considers:

- Armies already present
- Number of enemy neighbours
- Total armies in neighbouring enemy territories
- Estimated threat level

A simplified reinforcement score is:

```text
Total neighbouring enemy armies
-
Own armies
+
Number of enemy neighbours × 2
```

The agent reinforces the territory with the highest threat score.

### Attack scoring

The attack score considers:

- Army advantage
- Number of connections of the defending territory
- Bonus for attacking a territory with one army

A simplified attack score is:

```text
Army advantage × 3
+
Defending territory connection score
+
Capture bonus
```

The agent selects the valid attack with the highest positive score.

---

## 18. Monte Carlo Agent

The Monte Carlo Agent evaluates attacks through repeated random battle simulations.

For every valid attack, the agent:

1. Reads the attacking army count.
2. Reads the defending army count.
3. Creates simulated attacker and defender values.
4. Runs repeated dice battles.
5. Counts how frequently the territory is captured.
6. Records expected remaining armies.
7. Calculates an attack score.
8. Compares the score with the other valid attacks.

The current configuration uses:

```text
100 simulations per valid attack
```

The attack score is primarily based on:

```text
Capture probability × 100
+
Expected remaining-army difference
```

The agent stops when the best estimated capture probability is below:

```text
30%
```

This prevents it from selecting attacks considered excessively risky by its simulations.

---

## 19. Monte Carlo Scope

The current Monte Carlo Agent simulates local battle outcomes.

It does not simulate complete games from the current state until a final winner is reached.

This design was selected because it is simpler, easier to explain and less computationally expensive.

The Monte Carlo Agent should therefore be described as a simulation-based local decision agent rather than a full-game search agent.

A future Monte Carlo Tree Search agent could explore sequences of game states and actions.

---

## 20. Performance Metrics

The following metrics are collected for every player in every game:

### Outcome metrics

- Winner
- Winning agent
- Turns played
- Win rate
- Loss rate
- Draw rate

### Combat metrics

- Attacks made
- Successful attacks
- Attack success rate
- Armies lost
- Territories captured

### Computational metrics

- Decisions made
- Total decision time
- Average decision time
- Number of simulations performed

### Experimental-control metrics

- Player position
- Match number
- Game number
- Random seed
- Maximum turn limit

---

## 21. Successful-Attack Definition

A successful attack is recorded when the defender loses at least one army during a battle round.

This does not necessarily mean the territory was captured.

For example:

```text
Attacker rolls successfully
Defender loses one army
Defender still has armies remaining
```

This counts as a successful attack but not a territory capture.

---

## 22. Decision-Time Measurement

Decision time is measured using:

```python
time.perf_counter()
```

The timer starts immediately before the agent selects a decision and stops immediately after the decision is returned.

Decision time includes:

- Reinforcement selection
- Attack selection
- Monte Carlo simulation time

It does not include:

- Printing output
- Dice execution by the main game engine
- CSV writing
- Statistical analysis

Decision-time values may vary slightly depending on computer workload.

Therefore, decision time is used as an approximate computational-performance measure.

---

## 23. Experimental Pairings

The four agents create six unique pairings:

```text
Random Agent vs Rule-Based Agent
Random Agent vs Heuristic Agent
Random Agent vs Monte Carlo Agent
Rule-Based Agent vs Heuristic Agent
Rule-Based Agent vs Monte Carlo Agent
Heuristic Agent vs Monte Carlo Agent
```

Every pairing is evaluated independently.

---

## 24. High-Volume Evaluation

The final experiment uses:

```text
Games per pairing: 500
Number of pairings: 6
Total games: 3,000
Maximum turns per game: 100
Monte Carlo simulations per valid attack: 100
```

Each agent therefore participates in:

```text
Three pairings × 500 games = 1,500 games
```

This provides a larger evidence base than the earlier 20-game development experiments.

The final values should match the actual configuration used when the experiment is executed.

---

## 25. Starting-Position Control

Player 1 always takes the first turn.

This may create a first-player advantage.

To reduce this bias, agent positions alternate between games.

For example:

```text
Game 1:
Player 1 = Agent A
Player 2 = Agent B

Game 2:
Player 1 = Agent B
Player 2 = Agent A
```

With 500 games per pairing:

```text
Agent A starts first in 250 games
Agent B starts first in 250 games
```

This creates an equal distribution of starting positions.

---

## 26. Random-Seed Reproducibility

A unique fixed random seed is assigned to every game.

The seed is calculated using:

```python
game_seed = (
    base_seed
    + match_number * 100000
    + game_number
)
```

The fixed seed controls:

- Dice rolls
- Random Agent selections
- Monte Carlo simulation rolls

The seed used for each game is stored in the final CSV file.

Running the same code with the same seed should reproduce:

- The same winner
- The same number of turns
- The same attack sequence
- The same armies lost
- The same territory captures
- The same simulation count

Decision-time values may differ slightly because they are influenced by computer workload.

---

## 27. Raw Data Collection

Each completed game produces one row in:

```text
results/final_reproducible_tournament.csv
```

Each row includes:

- Match number
- Game number
- Global game number
- Random seed
- Agent names
- Player positions
- Winner
- Turns played
- Player 1 metrics
- Player 2 metrics

The raw result file is retained so the statistical results and graphs can be regenerated.

---

## 28. Statistical Analysis

The final analysis calculates:

- Total games
- Wins
- Losses
- Draws
- Win rate
- Loss rate
- Draw rate
- Mean game length
- Median game length
- Minimum game length
- Maximum game length
- Standard deviation of game length
- Attack success rate
- Average attacks per game
- Average armies lost
- Average territory captures
- Average decision time
- Average simulations per game
- Player 1 win rate
- Player 2 win rate

---

## 29. Confidence Intervals

The final analysis calculates 95% Wilson confidence intervals for agent win rates.

The Wilson interval is used because win rate is a proportion based on a finite number of games.

The confidence interval provides a range around the observed win rate.

For example:

```text
Observed win rate: 48%
95% confidence interval: 44% to 52%
```

This provides more information than reporting only the observed percentage.

---

## 30. Head-to-Head Analysis

Results are analysed separately for every agent pairing.

The head-to-head analysis records:

- Number of games
- Agent 1 wins
- Agent 2 wins
- Draws
- Agent 1 win rate
- Agent 2 win rate
- Draw rate

This helps identify whether an agent performs consistently or only performs well against particular opponents.

---

## 31. First-Player Analysis

The analysis separately records:

- Player 1 wins
- Player 2 wins
- Draws
- Overall Player 1 win rate
- Overall Player 2 win rate
- Each agent’s win rate when playing as Player 1
- Each agent’s win rate when playing as Player 2

This allows the study to investigate whether taking the first turn affects the result.

---

## 32. Automated Testing

The project uses Python’s built-in `unittest` framework.

The automated tests validate:

- Starting territory ownership
- Valid attack generation
- Reinforcement calculation
- Valid reinforcement
- Invalid reinforcement
- Defender advantage in equal dice
- Territory capture
- Invalid attack rejection
- Winner detection
- Game reset
- Metrics reset
- Fixed-seed reproducibility

The tests are run using:

```powershell
python -m unittest discover -s tests -v
```

---

## 33. Controlled Dice Testing

The territory-capture test replaces random dice results with predetermined values.

For example:

```text
Attacker dice: 6, 5, 4
Defender die: 1
```

This ensures that the expected capture result can be checked without relying on chance.

Controlled testing helps confirm that:

- Army losses are correctly applied
- Ownership is transferred
- One army moves into the captured territory
- Capture metrics are updated

---

## 34. Validation Procedure

The simulator was validated through:

1. Manual execution of individual functions.
2. Visible game runs.
3. Agent-versus-agent games.
4. Repeated small-scale experiments.
5. CSV inspection.
6. Automated unit tests.
7. Fixed-seed reproducibility tests.
8. High-volume evaluation.
9. Statistical result checks.

This combination of manual and automated validation improves confidence in the implementation.

---

## 35. Software Environment

The project uses:

- Python
- Visual Studio Code
- Python standard-library modules
- Matplotlib for graph generation

The standard-library modules include:

- random
- copy
- csv
- io
- os
- time
- statistics
- math
- itertools
- unittest
- platform

The exact Python version and operating system are automatically recorded in:

```text
results/final_evaluation_config.txt
```

---

## 36. Hardware Environment

The final experiment is executed on the researcher’s computer.

The final dissertation should report the actual hardware used, where available, including:

- Processor
- Installed memory
- Operating system
- Python version

The operating system and Python version are recorded automatically by the final evaluation script.

Decision-time results should be interpreted in relation to the hardware used.

---

## 37. Ethical Considerations

The project does not involve:

- Human participants
- Personal data
- Surveys
- Interviews
- Medical data
- Financial data
- Behavioural tracking

All experimental data are generated by the Python simulator.

The project therefore presents minimal ethical risk.

The main research-integrity requirements are:

- Accurately reporting the implemented rules
- Retaining raw result files
- Recording random seeds
- Reporting limitations
- Avoiding unsupported generalisation to the full commercial game

---

## 38. Reliability

Reliability is supported by:

- A common game engine for all agents
- Equal starting armies
- Equal starting territories
- Alternating player positions
- Fixed random seeds
- Repeated games
- Automated tests
- Raw-data storage
- Clearly defined performance metrics

---

## 39. Validity

### Internal validity

Internal validity is supported by controlling:

- Starting state
- Game rules
- Turn limit
- Number of simulations
- Agent positions
- Random seeds

The main difference between experimental conditions is the agent decision-making method.

### Construct validity

Performance is represented through multiple measures rather than win rate alone.

These include:

- Combat efficiency
- Territory capture
- Resource loss
- Game length
- Decision time
- Simulation count

### External validity

External validity is limited because the project uses a simplified six-territory, two-player environment.

The findings should not automatically be generalised to:

- The complete 42-territory board
- Games with more than two players
- Games with cards
- Games with continent bonuses
- Human RISK players

---

## 40. Methodological Limitations

The methodology has several limitations:

- The map contains only six territories.
- The game contains only two players.
- There is no fortification phase.
- There are no cards or card-trading mechanics.
- There are no continent bonuses.
- Reinforcement rules are scaled for the smaller map.
- Agents can make only five attack decisions per turn.
- The Monte Carlo Agent simulates local battles rather than complete games.
- Decision-time measurements are hardware-dependent.
- A turn limit can convert unresolved games into draws.
- Heuristic weights were manually selected.
- Monte Carlo simulation count was fixed at 100 per valid attack.

These limitations should be considered when interpreting the results.

---

## 41. Future Methodological Extensions

Future work could include:

- Monte Carlo Tree Search
- Full-game Monte Carlo rollouts
- Full 42-territory map
- Three or more players
- Continent bonuses
- Fortification phase
- Territory cards
- Reinforcement learning
- Sensitivity analysis of heuristic weights
- Sensitivity analysis of simulation counts
- Human-versus-agent experiments
- Multiple hardware environments
- Formal statistical significance tests between agents

---

## 42. Methodology Summary

The methodology combines:

```text
Controlled simulation
        +
Multiple AI agents
        +
Repeated experiments
        +
Alternating player positions
        +
Fixed random seeds
        +
Performance metrics
        +
Computational metrics
        +
Automated tests
        +
Statistical analysis
```

This approach provides a structured and reproducible framework for comparing AI decision-making methods in the implemented simplified RISK environment.