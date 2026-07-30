# Results

## 1. Introduction

This chapter presents the results of the experimental evaluation of four artificial intelligence agents implemented for the simplified RISK environment:

- Random Agent
- Rule-Based Agent
- Heuristic Agent
- Monte Carlo Agent

The agents were compared using repeated agent-versus-agent games under controlled conditions. The analysis examines overall win rate, loss rate, draw rate, game length, attack behaviour, armies lost, territories captured, decision time, Monte Carlo simulation cost, head-to-head performance, starting-position advantage and reproducibility.

The purpose of this chapter is to report the experimental findings. Interpretation of why the agents performed differently is reserved for the discussion chapter.

---

## 2. Final Experimental Dataset

The final evaluation included four agents and six unique agent pairings:

```text
Random Agent vs Rule-Based Agent
Random Agent vs Heuristic Agent
Random Agent vs Monte Carlo Agent
Rule-Based Agent vs Heuristic Agent
Rule-Based Agent vs Monte Carlo Agent
Heuristic Agent vs Monte Carlo Agent
```

Each pairing was evaluated across **500 games**, producing **3,000 games** in total. Each game used a maximum of **100 turns**, and the Monte Carlo Agent used **100 simulations per valid attack**. The agents alternated between Player 1 and Player 2 so that each agent received an equal opportunity to take the first turn.

The final evaluation used base random seed `20260730`, Python 3.14.0 and Windows 11. The complete raw dataset was stored in:

```text
results/final_reproducible_tournament.csv
```

---

## 3. Reproducibility Validation

A unique fixed random seed was assigned to every game.

### Table 1. Reproducibility validation

| Reproducibility measure | Result |
|---|---:|
| Total games | 3,000 |
| Seeds recorded | 3,000 |
| Unique seeds | 3,000 |
| Duplicate seeds | 0 |
| Minimum seed | 20,360,731 |
| Maximum seed | 20,861,230 |
| Seed validation | PASSED |

The seed-validation procedure confirmed that all 3,000 games used unique seeds and that no duplicate seeds were present.

When the same source code, agent configuration and random seed are used, the winner, number of turns, attacks made, successful attacks, armies lost, territory captures and simulations performed should be reproducible. Decision-time measurements may vary slightly because they depend on computer workload.

---

## 4. Overall Agent Performance

Table 2 presents the overall outcome performance of the four agents.

### Table 2. Overall agent outcomes

| Agent | Games | Wins | Losses | Draws | Win rate | Draw rate |
|---|---:|---:|---:|---:|---:|---:|
| Random Agent | 1,500 | 384 | 540 | 576 | 25.60% | 38.40% |
| Rule-Based Agent | 1,500 | 711 | 548 | 241 | 47.40% | 16.07% |
| Heuristic Agent | 1,500 | 577 | 713 | 210 | 38.47% | 14.00% |
| Monte Carlo Agent | 1,500 | 693 | 564 | 243 | 46.20% | 16.20% |

The **Rule-Based Agent** achieved the highest overall win rate, at **47.40%**. The **Monte Carlo Agent** achieved the second-highest rate, at **46.20%**. The **Random Agent** recorded the lowest win rate, at **25.60%**.

The Random Agent had the highest draw rate, at 38.40%, while the Heuristic Agent had the lowest, at 14.00%.

---

## 5. Win-Rate Confidence Intervals

The study calculated 95% Wilson confidence intervals for each agent’s observed win rate.

### Table 3. Win rates with 95% confidence intervals

| Agent | Win rate | Lower confidence limit | Upper confidence limit |
|---|---:|---:|---:|
| Random Agent | 25.60% | 23.46% | 27.87% |
| Rule-Based Agent | 47.40% | 44.88% | 49.93% |
| Heuristic Agent | 38.47% | 36.04% | 40.96% |
| Monte Carlo Agent | 46.20% | 43.69% | 48.73% |

The narrowest confidence interval was recorded for the **Random Agent**, with a width of 4.41 percentage points. The widest was recorded for the **Rule-Based Agent**, with a width of 5.05 percentage points.

The Rule-Based and Monte Carlo confidence intervals overlap substantially. Therefore, the observed difference of 1.20 percentage points between their overall win rates should be interpreted cautiously.

Insert the following graph:

```text
results/final_graphs/win_rate_confidence_intervals.png
```

### Figure 1. Agent win rates with 95% confidence intervals

Figure 1 shows the overall win rate of each agent together with its corresponding 95% Wilson confidence interval.

---

## 6. Head-to-Head Results

The overall results were separated into the six individual agent pairings.

### Table 4. Head-to-head agent performance

| Agent 1 | Agent 2 | Games | Agent 1 wins | Agent 2 wins | Draws | Agent 1 win rate | Agent 2 win rate | Draw rate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Random Agent | Rule-Based Agent | 500 | 122 | 182 | 196 | 24.40% | 36.40% | 39.20% |
| Random Agent | Heuristic Agent | 500 | 140 | 184 | 176 | 28.00% | 36.80% | 35.20% |
| Random Agent | Monte Carlo Agent | 500 | 122 | 174 | 204 | 24.40% | 34.80% | 40.80% |
| Rule-Based Agent | Heuristic Agent | 500 | 279 | 201 | 20 | 55.80% | 40.20% | 4.00% |
| Rule-Based Agent | Monte Carlo Agent | 500 | 250 | 225 | 25 | 50.00% | 45.00% | 5.00% |
| Heuristic Agent | Monte Carlo Agent | 500 | 192 | 294 | 14 | 38.40% | 58.80% | 2.80% |

The largest head-to-head difference occurred between the **Monte Carlo Agent and Heuristic Agent**. In this pairing, the Monte Carlo Agent won **58.80%** of games, the Heuristic Agent won **38.40%**, and **2.80%** ended in draws. The difference between their win rates was 20.40 percentage points.

The most balanced pairing was the **Rule-Based Agent versus Monte Carlo Agent**. The Rule-Based Agent won 50.00%, the Monte Carlo Agent won 45.00%, and 5.00% ended in draws.

---

## 7. Game-Length Results

Game length was measured using the number of turns completed before a player won or the maximum turn limit was reached.

### Table 5. Game-length statistics

| Agent | Mean turns | Median turns | Standard deviation | Minimum turns | Maximum turns |
|---|---:|---:|---:|---:|---:|
| Random Agent | 66.45 | 73.0 | 33.09 | 4 | 100 |
| Rule-Based Agent | 47.75 | 39.0 | 30.89 | 5 | 100 |
| Heuristic Agent | 45.46 | 35.5 | 30.76 | 4 | 100 |
| Monte Carlo Agent | 49.30 | 41.0 | 30.70 | 4 | 100 |

The shortest average game length was associated with the **Heuristic Agent**, at **45.46 turns**. The longest was associated with the **Random Agent**, at **66.45 turns**.

Games involving the Random Agent also had the highest median duration, at 73 turns, which is consistent with its higher draw rate.

---

## 8. Draw Rates

A game was recorded as a draw when neither player controlled all six territories before reaching the 100-turn limit.

### Table 6. Agent draw rates

| Agent | Draws | Draw rate |
|---|---:|---:|
| Random Agent | 576 | 38.40% |
| Rule-Based Agent | 241 | 16.07% |
| Heuristic Agent | 210 | 14.00% |
| Monte Carlo Agent | 243 | 16.20% |

The highest draw rate was recorded by the **Random Agent**, at **38.40%**. The lowest was recorded by the **Heuristic Agent**, at **14.00%**.

Insert the following graph:

```text
results/final_graphs/draw_rate.png
```

### Figure 2. Agent draw rates

Figure 2 compares how frequently games involving each agent reached the maximum turn limit.

---

## 9. Attack Frequency

The average number of attack rounds performed per game was calculated for each agent.

### Table 7. Average attacks per game

| Agent | Average attacks per game |
|---|---:|
| Random Agent | 31.07 |
| Rule-Based Agent | 25.99 |
| Heuristic Agent | 24.44 |
| Monte Carlo Agent | 26.87 |

The most active attacking agent was the **Random Agent**, with an average of **31.07 attacks per game**. The least active was the **Heuristic Agent**, with an average of **24.44 attacks per game**.

Attack frequency alone does not demonstrate effectiveness and must be considered alongside attack success, army losses, territory captures and overall outcomes.

---

## 10. Attack Success Rate

A successful attack was defined as a battle round in which the defender lost at least one army.

### Table 8. Attack success rates

| Agent | Attack success rate |
|---|---:|
| Random Agent | 55.32% |
| Rule-Based Agent | 49.55% |
| Heuristic Agent | 45.62% |
| Monte Carlo Agent | 48.33% |

The highest attack success rate was achieved by the **Random Agent**, at **55.32%**. The lowest was recorded by the **Heuristic Agent**, at **45.62%**.

Although the Random Agent had the highest attack success rate, it also had the lowest overall win rate. This result shows that success in an individual battle round is not the same as success across the complete game.

Insert the following graph:

```text
results/final_graphs/attack_success_rate.png
```

### Figure 3. Agent attack success rates

Figure 3 compares the proportion of attack rounds in which each agent caused the defender to lose at least one army.

---

## 11. Armies Lost

The average number of armies lost per game was calculated for each agent.

### Table 9. Average armies lost per game

| Agent | Average armies lost |
|---|---:|
| Random Agent | 34.40 |
| Rule-Based Agent | 28.46 |
| Heuristic Agent | 28.35 |
| Monte Carlo Agent | 29.42 |

The **Heuristic Agent** lost the fewest armies per game on average, at **28.35**. The **Random Agent** lost the most, at **34.40**.

---

## 12. Territory-Capture Performance

The average number of territory-capture events per game was calculated for each agent.

### Table 10. Average territory captures

| Agent | Average territories captured per game |
|---|---:|
| Random Agent | 13.54 |
| Rule-Based Agent | 11.67 |
| Heuristic Agent | 10.24 |
| Monte Carlo Agent | 12.18 |

The **Random Agent** achieved the largest average number of territory-capture events, at **13.54 per game**. The **Heuristic Agent** achieved the smallest average, at **10.24**.

The number of capture events may be greater than six because territories can be captured, lost and recaptured during the same game.

---

## 13. Computational Decision Time

Decision time was measured using `time.perf_counter()` and converted from seconds to milliseconds.

### Table 11. Average decision time

| Agent | Average decision time |
|---|---:|
| Random Agent | 0.004258 milliseconds |
| Rule-Based Agent | 0.005101 milliseconds |
| Heuristic Agent | 0.005598 milliseconds |
| Monte Carlo Agent | 0.749225 milliseconds |

The fastest agent was the **Random Agent**, with an average decision time of **0.004258 milliseconds**. The slowest was the **Monte Carlo Agent**, with an average of **0.749225 milliseconds**.

The Monte Carlo Agent required substantially more decision time because it ran repeated simulated battles before selecting an attack.

Insert the following graph:

```text
results/final_graphs/decision_time.png
```

### Figure 4. Average decision time by agent

Figure 4 demonstrates the computational difference between direct decision rules and simulation-based decision-making. Decision-time results should be interpreted in relation to the hardware and workload of the computer used for the experiment.

---

## 14. Monte Carlo Simulation Cost

The number of simulations performed by each agent was recorded.

### Table 12. Average simulations per game

| Agent | Average simulations per game |
|---|---:|
| Random Agent | 0 |
| Rule-Based Agent | 0 |
| Heuristic Agent | 0 |
| Monte Carlo Agent | 4,572.60 |

Only the Monte Carlo Agent performed battle simulations. It completed an average of **4,572.60 simulations per game**.

Insert the following graph:

```text
results/final_graphs/simulations_per_game.png
```

### Figure 5. Average simulations performed per game

Figure 5 shows the additional computational work performed by the Monte Carlo Agent.

---

## 15. Starting-Position Analysis

Player 1 always acted first. The agents alternated between Player 1 and Player 2 positions to reduce starting-position bias.

### Table 13. Overall starting-position results

| Measure | Result |
|---|---:|
| Total games | 3,000 |
| Player 1 wins | 1,363 |
| Player 2 wins | 1,002 |
| Draws | 635 |
| Player 1 win rate | 45.43% |
| Player 2 win rate | 33.40% |
| Player 1 win rate among decisive games | 57.63% |

Player 1 won **45.43%** of all games, while Player 2 won **33.40%**. The difference between the two positions was **12.03 percentage points**. Among games that produced a winner, Player 1 won 57.63%.

These results indicate a measurable first-player advantage in the implemented environment, despite alternating agent positions during the experiment.

---

## 16. Agent Performance by Starting Position

### Table 14. Agent win rates by player position

| Agent | Win rate as Player 1 | Win rate as Player 2 | Absolute difference |
|---|---:|---:|---:|
| Random Agent | 35.60% | 15.60% | 20.00 percentage points |
| Rule-Based Agent | 52.80% | 42.00% | 10.80 percentage points |
| Heuristic Agent | 42.53% | 34.40% | 8.13 percentage points |
| Monte Carlo Agent | 50.80% | 41.60% | 9.20 percentage points |

Insert the following graph:

```text
results/final_graphs/starting_position_comparison.png
```

### Figure 6. Agent performance by starting position

Figure 6 compares how each agent performed when moving first and when moving second.

The **Random Agent** was most affected by starting position, with a difference of 20.00 percentage points. The **Heuristic Agent** was least affected, with a difference of 8.13 percentage points.

---

## 17. Performance Ranking

Based on overall win rate, the agents were ranked as follows:

### Table 15. Overall ranking by win rate

| Rank | Agent | Win rate |
|---:|---|---:|
| 1 | Rule-Based Agent | 47.40% |
| 2 | Monte Carlo Agent | 46.20% |
| 3 | Heuristic Agent | 38.47% |
| 4 | Random Agent | 25.60% |

The ranking shows that the **Rule-Based Agent** achieved the strongest overall outcome performance. However, the Rule-Based and Monte Carlo confidence intervals overlap, so the difference between them should not be treated as conclusive without an additional inferential comparison.

---

## 18. Performance and Computational-Cost Comparison

### Table 16. Combined strategic and computational performance

| Agent | Win rate | Attack success | Decision time | Simulations per game |
|---|---:|---:|---:|---:|
| Random Agent | 25.60% | 55.32% | 0.004258 ms | 0 |
| Rule-Based Agent | 47.40% | 49.55% | 0.005101 ms | 0 |
| Heuristic Agent | 38.47% | 45.62% | 0.005598 ms | 0 |
| Monte Carlo Agent | 46.20% | 48.33% | 0.749225 ms | 4,572.60 |

The **Rule-Based Agent** achieved the best observed balance between overall win rate and decision time: it recorded the highest win rate while requiring only 0.005101 milliseconds per decision on average.

The Monte Carlo Agent used substantially more computational resources than the other agents. Its additional cost produced a win rate slightly below that of the Rule-Based Agent, but above those of the Heuristic and Random Agents.

---

## 19. Summary of Main Results

The main findings were:

1. The highest overall win rate was achieved by the **Rule-Based Agent**, at **47.40%**.
2. The lowest overall win rate was recorded by the **Random Agent**, at **25.60%**.
3. The highest attack success rate was achieved by the **Random Agent**, at **55.32%**.
4. The lowest average decision time was recorded by the **Random Agent**, at **0.004258 milliseconds**.
5. The Monte Carlo Agent performed an average of **4,572.60 simulations per game**.
6. Player 1 won **45.43%** of all games, compared with **33.40%** for Player 2.
7. The overall draw rate was **21.17%**.
8. All 3,000 final games were assigned unique fixed random seeds.
9. The reproducibility seed-validation result was **PASSED**.
10. The strongest head-to-head advantage occurred in the **Monte Carlo Agent versus Heuristic Agent** comparison, where the Monte Carlo Agent led by 20.40 percentage points.

These findings will be interpreted in the discussion chapter by considering the decision logic, computational cost, first-player advantage and limitations of the simplified environment.

---

## Data Sources

This chapter was completed using:

```text
results/final_agent_summary.csv
results/final_head_to_head_summary.csv
results/final_starting_position_summary.csv
results/reproducibility_report.txt
results/final_evaluation_config.txt
```
