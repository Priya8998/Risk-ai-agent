# RISK AI Project Architecture

## 1. Architecture Overview

The project separates the AI decision-making logic from the RISK game rules.

The agents only select actions. The game engine validates and executes those actions.

```text
                   Experiment Runner
                           |
                           v
                   Select Two Agents
                           |
                           v
                Current RISK Game State
                           |
                           v
      ------------------------------------------------
      | Random | Rule-Based | Heuristic | Monte Carlo |
      ------------------------------------------------
                           |
                           v
                  Agent Selects Action
                           |
                           v
                    RISK Game Engine
                           |
          ----------------------------------
          | Reinforcement                  |
          | Attack validation              |
          | Dice combat                    |
          | Army updates                   |
          | Territory capture              |
          | Winner detection               |
          ----------------------------------
                           |
                           v
                    Metrics Collector
                           |
                           v
                    CSV Result Files
                           |
                           v
              Statistical Analysis and Graphs
```

---

## 2. Main System Components

The project contains five main architectural components:

1. Game engine
2. AI agents
3. Experiment runners
4. Metrics and result storage
5. Statistical analysis and visualisation

---

## 3. Game Engine

The main game engine is implemented in:

```text
risk_game.py
```

The game engine is responsible for:

- Storing the map
- Storing territory ownership
- Storing army numbers
- Calculating reinforcements
- Identifying valid attacks
- Rolling combat dice
- Comparing dice results
- Removing lost armies
- Capturing territories
- Alternating player turns
- Detecting the winner
- Resetting the game
- Recording game metrics

The game engine controls the official state of the game.

Agents cannot directly modify territory ownership or army values.

---

## 4. Game-State Structure

The simplified map is stored as a Python dictionary.

Example:

```python
territories = {
    "A": {
        "owner": "Player 1",
        "armies": 3,
        "neighbours": ["B", "C"]
    }
}
```

Every territory contains:

```text
Territory name
    |
    |-- Owner
    |-- Number of armies
    |-- List of neighbouring territories
```

This structure allows the game engine to determine:

- Which player owns a territory
- Whether an attack is valid
- Which territories border an enemy
- How many armies can participate in combat

---

## 5. Simplified Map

```text
          A
         / \
        B---C
        |   |
        D---E
         \ /
          F
```

Starting ownership:

```text
Player 1: A, B, C
Player 2: D, E, F
```

Starting armies:

```text
Three armies on every territory
```

---

## 6. Agent Architecture

The agents are stored inside:

```text
agents/
```

```text
agents/
├── __init__.py
├── random_agent.py
├── rule_based_agent.py
├── heuristic_agent.py
└── monte_carlo_agent.py
```

Each agent contains functions for:

```text
Choosing a reinforcement territory
Choosing an attack
Choosing whether to stop attacking
```

---

## 7. Random Agent

File:

```text
agents/random_agent.py
```

Decision process:

```text
Observe owned territories
        |
        v
Randomly select reinforcement territory
        |
        v
Receive valid attacks from game engine
        |
        v
Randomly select attack or stop
```

The Random Agent is used as the baseline agent.

It does not evaluate army strength, territory importance or future outcomes.

---

## 8. Rule-Based Agent

File:

```text
agents/rule_based_agent.py
```

Decision process:

```text
Find border territories
        |
        v
Choose strongest border territory
        |
        v
Find valid attacks
        |
        v
Remove attacks where attacker is not stronger
        |
        v
Attack weakest suitable enemy
```

The Rule-Based Agent uses fixed decision rules.

It does not score all options or simulate future outcomes.

---

## 9. Heuristic Agent

File:

```text
agents/heuristic_agent.py
```

Decision process:

```text
Observe game state
        |
        v
Calculate reinforcement score
        |
        v
Select highest-scoring reinforcement territory
        |
        v
Calculate score for every valid attack
        |
        v
Select highest-scoring attack
```

The heuristic reinforcement score considers:

- Number of enemy neighbours
- Total enemy armies
- Armies already present
- Threat level

The heuristic attack score considers:

- Attacking-army advantage
- Defending-army strength
- Territory connectivity
- Capture opportunity

---

## 10. Monte Carlo Agent

File:

```text
agents/monte_carlo_agent.py
```

Decision process:

```text
Receive all valid attacks
        |
        v
Select first possible attack
        |
        v
Run repeated random battle simulations
        |
        v
Estimate capture probability
        |
        v
Estimate remaining armies
        |
        v
Repeat for every possible attack
        |
        v
Select attack with best simulation score
```

The Monte Carlo Agent currently performs:

```text
100 simulations for every valid attack
```

Its attack score is based mainly on:

```text
Estimated capture probability
+
Expected remaining-army advantage
```

It stops attacking when the estimated capture probability is below the configured threshold.

---

## 11. Turn Architecture

A complete agent turn follows this sequence:

```text
Start turn
    |
    v
Agent observes current state
    |
    v
Agent selects reinforcement territory
    |
    v
Game engine calculates reinforcement amount
    |
    v
Game engine adds reinforcement armies
    |
    v
Game engine calculates valid attacks
    |
    v
Agent selects attack or stop
    |
    v
Game engine validates selected attack
    |
    v
Game engine rolls dice
    |
    v
Game engine removes lost armies
    |
    v
Game engine checks for territory capture
    |
    v
Game engine checks for winner
    |
    v
Agent may make another attack decision
    |
    v
End turn
```

An agent can make up to five attack decisions during one turn.

The valid attack list is recalculated after every battle.

This allows an agent to use newly captured territories during the same turn.

---

## 12. Combat Architecture

```text
Attacker selects neighbouring enemy territory
                    |
                    v
Game engine validates the attack
                    |
                    v
Attacker rolls up to three dice
                    |
                    v
Defender rolls up to two dice
                    |
                    v
Dice are sorted from highest to lowest
                    |
                    v
Highest dice are compared
                    |
                    v
Equal dice are won by the defender
                    |
                    v
Armies are removed
                    |
                    v
Defender reaches zero armies?
          |                         |
         No                        Yes
          |                         |
          v                         v
 Continue battle          Transfer territory ownership
                                    |
                                    v
                       Move one attacking army into it
```

---

## 13. Experiment Architecture

The development experiment is implemented in:

```text
experiments.py
```

It compares two selected agents.

```text
Choose Agent A and Agent B
            |
            v
Run repeated games
            |
            v
Alternate Player 1 and Player 2 positions
            |
            v
Collect winner, turns and metrics
            |
            v
Save results to CSV
```

---

## 14. Tournament Architecture

The tournament is implemented in:

```text
tournament.py
```

With four agents, the program automatically creates six pairings:

```text
Random vs Rule-Based
Random vs Heuristic
Random vs Monte Carlo
Rule-Based vs Heuristic
Rule-Based vs Monte Carlo
Heuristic vs Monte Carlo
```

The tournament process is:

```text
List all agents
      |
      v
Create every unique pair
      |
      v
Run repeated games for each pair
      |
      v
Alternate starting positions
      |
      v
Save every result
      |
      v
Create overall performance summary
```

---

## 15. Final Reproducible Evaluation

The final high-volume experiment is implemented in:

```text
final_evaluation.py
```

Its responsibilities are:

- Run every agent pairing
- Run hundreds of games per pairing
- Alternate player positions
- Assign a unique fixed random seed to every game
- Record the complete agent configuration
- Save raw performance metrics
- Save computational metrics
- Save the experimental environment configuration

The seed-generation structure is:

```text
Base seed
    +
Match number
    +
Game number
    =
Unique reproducible game seed
```

Example:

```python
game_seed = (
    base_seed
    + match_number * 100000
    + game_number
)
```

---

## 16. Reproducibility Architecture

```text
Fixed random seed
        |
        v
Controls dice rolls
        |
        v
Controls Random Agent choices
        |
        v
Controls Monte Carlo simulations
        |
        v
Produces repeatable game outcome
```

The same code and seed should reproduce:

- Winner
- Turns played
- Attacks
- Armies lost
- Territories captured
- Simulations performed

Decision time may vary slightly because it depends on computer workload.

---

## 17. Metrics Architecture

The game engine records metrics separately for Player 1 and Player 2.

```text
game_metrics
|
|-- Player 1
|   |-- attacks_made
|   |-- successful_attacks
|   |-- armies_lost
|   |-- territories_captured
|   |-- decisions_made
|   |-- decision_time_seconds
|   |-- simulations_run
|
|-- Player 2
    |-- attacks_made
    |-- successful_attacks
    |-- armies_lost
    |-- territories_captured
    |-- decisions_made
    |-- decision_time_seconds
    |-- simulations_run
```

Metrics are reset at the beginning of every game.

A deep copy is returned at the end of the game so later resets do not change saved results.

---

## 18. Result-Processing Architecture

```text
Raw game results
        |
        v
final_reproducible_tournament.csv
        |
        v
final_analysis.py
        |
        |-- Overall agent summary
        |-- Head-to-head analysis
        |-- Starting-position analysis
        |-- Confidence intervals
        |-- Reproducibility report
        |
        v
Final CSV tables and graphs
```

---

## 19. Statistical Analysis

The final analysis calculates:

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
- Standard deviation
- Attack success rate
- Average armies lost
- Average territories captured
- Average decision time
- Average simulations
- First-player win rate
- Second-player win rate
- 95% Wilson confidence intervals

---

## 20. Testing Architecture

Automated tests are stored in:

```text
tests/test_risk_game.py
```

The tests validate:

```text
Starting ownership
Valid attack generation
Reinforcement calculation
Valid reinforcement
Invalid reinforcement
Dice tie rule
Territory capture
Invalid attack rejection
Winner detection
Game reset
Metrics reset
Seed reproducibility
```

Test flow:

```text
Reset game before every test
            |
            v
Create controlled game condition
            |
            v
Run one function
            |
            v
Compare actual result with expected result
            |
            v
Pass or fail
```

---

## 21. Complete Data Flow

```text
Game configuration
        |
        v
Fixed random seed
        |
        v
Initial game state
        |
        v
Agent observes state
        |
        v
Agent selects decision
        |
        v
Game engine executes decision
        |
        v
New game state
        |
        v
Metrics updated
        |
        v
Repeat until win or turn limit
        |
        v
Return winner, turns and metrics
        |
        v
Save one CSV row
        |
        v
Repeat across all games
        |
        v
Statistical analysis
        |
        v
Tables and graphs
        |
        v
Dissertation findings
```

---

## 22. Methodology Flow

```text
Define simplified RISK environment
                |
                v
Implement and validate game rules
                |
                v
Develop Random Agent baseline
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
Create common performance metrics
                |
                v
Run small development experiments
                |
                v
Add fixed random seeds
                |
                v
Run high-volume final evaluation
                |
                v
Perform statistical analysis
                |
                v
Compare performance and computational cost
                |
                v
Discuss findings and limitations
```

---

## 23. Design Principles

The architecture follows these principles:

### Separation of concerns

Game rules, agent decisions, experiments and analysis are stored separately.

### Fairness

Every agent uses the same game engine and follows the same rules.

### Reproducibility

Every final game records a fixed random seed.

### Modularity

New agents can be added without rewriting the complete game engine.

### Testability

Core game rules are validated through automated tests.

### Explainability

Every agent uses decision logic that can be inspected and explained.

---

## 24. Current Limitations

The current architecture does not include:

- Full 42-territory map
- More than two players
- Continent bonuses
- Territory cards
- Card trading
- Fortification phase
- Monte Carlo Tree Search
- Reinforcement learning
- Graphical player interface

These are possible future extensions.

---

## 25. Future MCTS Integration

A future Monte Carlo Tree Search agent could be added as:

```text
Current game state
        |
        v
Selection
        |
        v
Expansion
        |
        v
Simulation
        |
        v
Backpropagation
        |
        v
Best action
```

The new agent would be stored in:

```text
agents/mcts_agent.py
```

It could be connected to the existing `play_agent_turn()` function and automatically included in the tournament.