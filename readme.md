# Poker_Sim

A modular Texas Hold'em simulation, hand-evaluation, and equity-analysis engine built in Python.

Poker_Sim supports Monte Carlo simulation, exact enumeration, blocker-aware opponent ranges, multi-opponent equity analysis, and multiple hand-evaluation architectures ranging from a readable reference implementation to a performance-oriented evaluator capable of evaluating 5-card hands at over **2.7 million hands per second**.

## Features

* Texas Hold'em hand evaluation for 5-, 6-, and 7-card hands
* Reference, optimized, and high-performance evaluators
* Monte Carlo equity simulation
* Exact enumeration for tractable game states
* Known and random opponent support
* Partial and complete board support
* Multi-opponent simulation
* Opponent range parsing
* Blocker-aware range filtering
* Hand-vs-range equity analysis
* Preflop range notation including `TT+`, `ATs+`, `K9o+`, and `22-66`
* Win, tie, loss, and total-equity statistics
* Interactive command-line equity calculator
* Automated testing with `pytest`
* Evaluator performance benchmarking against Treys

---

## Quick Example

Estimate the equity of pocket Aces against an opponent range:

```python
from poker import cards
from poker.simulation import simulator

hero = cards.make_cards([
    "A of Spades",
    "A of Hearts"
])

wins, ties, losses = simulator.simulate_equity_vs_range(
    hero,
    "TT+, AKs, AKo",
    num_trials=100_000
)

results = simulator.calculate_equity_stats(
    wins,
    ties,
    losses
)

print(f"Win:    {results['win_rate']:.2%}")
print(f"Tie:    {results['tie_rate']:.2%}")
print(f"Loss:   {results['loss_rate']:.2%}")
print(f"Equity: {results['equity']:.2%}")
```

---

## Range Support

Poker_Sim supports common preflop poker range notation.

```text
AA          Pocket Aces
AKs         Ace-King suited
AKo         Ace-King offsuit
AK          All Ace-King combinations

TT+         TT, JJ, QQ, KK, AA
ATs+        ATs, AJs, AQs, AKs
K9o+        K9o, KTo, KJo, KQo

22-66       22, 33, 44, 55, 66
```

Ranges can be combined:

```text
TT+, AQs+, AKo
```

The parser expands each abstract hand class into physical two-card combinations and removes combinations blocked by known cards.

This allows simulations to account for blockers from the hero's hand and board before selecting an opponent holding.

---

## Hand Evaluation

Poker_Sim contains three evaluator implementations with different design goals.

### Reference Evaluator

`poker/evaluation/evaluator.py`

The reference evaluator prioritizes readability and correctness.

Hands are evaluated into lexicographically comparable tuples representing:

```text
High Card
One Pair
Two Pair
Three of a Kind
Straight
Flush
Full House
Four of a Kind
Straight Flush
```

Special cases such as the wheel straight are supported:

```text
A-2-3-4-5
```

The reference implementation also serves as an independent correctness baseline for the optimized evaluators.

### Fast Evaluator

`poker/evaluation/fast_evaluator.py`

The Fast evaluator replaces much of the branching logic with precomputed lookup tables.

Five-card hands are encoded using rank-based prime products, which map directly to precomputed hand scores.

For 6- and 7-card hands, the evaluator examines the possible five-card subsets and returns the strongest result.

This significantly reduces the cost of five-card hand evaluation while maintaining the same output format as the reference implementation.

### Lightning Evaluator

`poker/evaluation/lightning_evaluator.py`

The Lightning evaluator is the performance-oriented implementation.

Rather than forcing every hand size through the same algorithm, Lightning uses specialized strategies based on the number of cards being evaluated:

* **5 cards:** optimized prime-product lookup
* **6 cards:** explicitly evaluates the six possible five-card subsets with an unrolled hot path
* **7 cards:** direct evaluation using precomputed rank and suit bitmasks and lookup tables

The 7-card evaluator avoids evaluating all 21 possible five-card subsets.

Instead, it constructs rank and suit information once and directly resolves the strongest available poker category.

Precomputed tables are used for operations including:

* Straight detection
* Flush evaluation
* Top-rank selection
* Kicker extraction
* Rank-mask evaluation

This reduces redundant work and substantially improves performance for full Texas Hold'em hands.

---

## Performance

Poker_Sim includes benchmarking against both the internal Fast evaluator and the external Python poker evaluator [Treys](https://github.com/ihendley/treys).

The benchmark uses the same randomly generated hands for every evaluator.

Treys card conversion is performed **outside the timed section**, so the results measure hand-evaluation performance rather than representation-conversion overhead.

Each benchmark below uses:

* **1,000,000 hands per run**
* **5 repetitions**
* Median throughput
* Identical hands across evaluators
* Warmup evaluations before timing

### Benchmark Results

| Hand Size |                Fast |               Lightning |               Treys | Lightning vs. Treys | Lightning vs. Fast |
| --------- | ------------------: | ----------------------: | ------------------: | ------------------: | -----------------: |
| 5-card    | 2,536,281 hands/sec | **2,751,355 hands/sec** | 1,119,884 hands/sec |           **2.46x** |          **1.08x** |
| 6-card    |   303,343 hands/sec |   **477,937 hands/sec** |   213,704 hands/sec |           **2.24x** |          **1.58x** |
| 7-card    |   114,298 hands/sec |   **237,880 hands/sec** |    70,551 hands/sec |           **3.37x** |          **2.08x** |

The largest relative improvement appears in 7-card evaluation, where the Lightning evaluator is:

* **3.37x faster than Treys**
* **2.08x faster than Poker_Sim's Fast evaluator**

The 5-card Lightning evaluator exceeds **2.75 million hand evaluations per second**.

The 6-card specialized path reaches approximately **478,000 evaluations per second**, more than **58% faster** than the general subset-based Fast evaluator.

Run the benchmark from the repository root:

```bash
python3 -m benchmarks.benchmark
```

---

## Equity Simulation

Poker_Sim supports equity calculation against random opponents, known hands, and specified opponent ranges.

### Hero vs. Random Opponent

```python
simulator.simulate_equity(
    hero,
    num_random_opponents=1,
    num_trials=100_000
)
```

### Hero vs. Known Opponent

```python
simulator.simulate_equity(
    hero,
    known_opponent_hands=[villain],
    num_trials=100_000
)
```

### Hero vs. Range

```python
simulator.simulate_equity_vs_range(
    hero,
    "QQ+, AQs+, AKo",
    known_board=board,
    num_trials=100_000
)
```

For hand-vs-range simulation, each trial:

1. Expands the opponent range into legal physical combinations
2. Removes combinations blocked by known cards
3. Samples an opponent hand
4. Removes all known cards from the remaining deck
5. Completes the board
6. Evaluates the showdown
7. Records a win, tie, or loss

The resulting outcomes can then be converted into win rate, tie rate, loss rate, and total equity.

---

## Exact Enumeration

Monte Carlo simulation is useful when the number of possible outcomes is large, but sampling is unnecessary when the remaining state space is small enough to enumerate completely.

Poker_Sim supports exact enumeration for tractable game states.

This allows the engine to calculate exact equity when enumeration is practical while retaining Monte Carlo simulation for larger game states.

```text
Large search space  -> Monte Carlo simulation
Small search space  -> Exact enumeration
```

---

## Command-Line Demo

Poker_Sim includes an interactive equity calculator in:

```text
examples/equity_cli.py
```

Run it from the repository root:

```bash
python3 -m examples.equity_cli
```

Example session:

```text
Poker_Sim Equity Calculator
---------------------------
Hero hand (e.g. As Kh): As Ah
Board (e.g. Qs 7d 2s, or leave blank): Qs 7d 2s
Opponent range (e.g. TT+, AQs+, AKo): TT+, AQs+, AKo
Number of trials [20000]: 100000

Results
-------
Win:    61.40%
Tie:     4.20%
Loss:   34.40%
Equity: 63.50%
Trials: 100,000
```

The CLI supports short-form card notation such as:

```text
As Ah Kd Tc 7s
```

---

## Project Structure

```text
Poker_Sim/
├── poker/
│   ├── cards.py
│   ├── deck.py
│   ├── hand.py
│   │
│   ├── evaluation/
│   │   ├── evaluator.py
│   │   ├── fast_evaluator.py
│   │   └── lightning_evaluator.py
│   │
│   ├── simulation/
│   │   ├── simulator.py
│   │   └── exact_solver.py
│   │
│   └── ranges/
│       └── range.py
│
├── examples/
│   └── equity_cli.py
│
├── tests/
│   ├── test_evaluator_consistency.py
│   ├── test_hand.py
│   ├── test_range.py
│   └── test_simulator.py
│
├── benchmarks/
│   ├── benchmark.py
│   └── compare_treys.py
│
└── README.md
```

---

## Testing

Poker_Sim uses `pytest` for automated correctness testing.

The test suite covers:

* Every major poker hand category
* Wheel straights and straight flushes
* Hand-ranking ordering
* Reference vs. optimized evaluator consistency
* Randomized evaluator comparisons
* Deck preparation
* Board completion
* Multi-opponent dealing
* Win, tie, and loss scoring
* Exact-solver integration
* Monte Carlo simulation
* Range parsing
* Plus notation
* Interval notation
* Duplicate range handling
* Invalid range detection
* Blocker handling
* Hand-vs-range simulation
* Guaranteed win, loss, and tie scenarios

Run the complete suite with:

```bash
python3 -m pytest -v
```

The independent evaluator implementations provide an additional correctness check: optimized evaluators can be compared against the simpler reference implementation across randomly generated hands.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/aryan-moore/Poker_Sim.git
cd Poker_Sim
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install testing dependencies:

```bash
pip install pytest
```

To run benchmarks against Treys:

```bash
pip install treys
```

Run the test suite:

```bash
python3 -m pytest -v
```

Run the evaluator benchmark:

```bash
python3 -m benchmarks.benchmark
```

---

## Design

Poker_Sim separates card representation, evaluation, simulation, and range analysis into independent modules.

```text
Cards / Deck
      |
      v
Hand Construction
      |
      v
Hand Evaluation
      |
      v
Exact Enumeration / Monte Carlo Simulation
      |
      v
Range Parsing + Blocker Filtering
      |
      v
Equity Analysis
```

Maintaining independent reference and optimized evaluators provides a useful correctness strategy: performance-oriented implementations can be checked against a simpler evaluator rather than relying only on manually constructed expected outputs.

The Lightning evaluator extends this approach by treating performance as an algorithm-selection problem.

Different hand sizes use different strategies based on which approach performs best:

```text
5 cards -> Prime-product lookup
6 cards -> Specialized six-subset evaluation
7 cards -> Direct rank/suit mask evaluation
```

This allows the implementation to optimize the most common operations without requiring every hand size to use the same evaluation strategy.

---

## Roadmap

Potential future additions include:

* Weighted opponent ranges
* Range-vs-range equity analysis
* Equity visualization
* Improved command-line tooling
* Web-based equity calculator
* REST API
* Further evaluator optimization
* Automated poker agents for simulation and permitted competition environments

---

## Author

**Aryan Moore**
Computer Science
Princeton University
