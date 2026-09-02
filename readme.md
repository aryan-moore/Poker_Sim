# Poker_Sim

A modular Texas Hold'em simulation and equity analysis engine built in Python.

Poker_Sim supports hand evaluation, Monte Carlo simulation, exact enumeration, opponent range parsing, blocker-aware range filtering, hand-vs-range equity analysis, and a command-line demo for interactive use.

## Features

- Texas Hold'em hand evaluation
- Reference and optimized evaluators
- Monte Carlo equity simulation
- Exact enumeration for tractable game states
- Known and random opponent support
- Partial and complete board support
- Opponent range parsing
- Plus notation such as `TT+`, `ATs+`, and `K9o+`
- Interval notation such as `22-66`
- Blocker-aware range filtering
- Hand-vs-range equity simulation
- Multi-opponent simulation
- Equity statistics including win, tie, loss, and total equity
- Command-line equity calculator demo
- Automated testing with pytest
- Evaluator performance benchmarking

## Range Support

Poker_Sim supports common preflop range notation.

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

## Example

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
    num_trials=100000
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

## Command-Line Demo

Poker_Sim includes a simple interactive CLI demo in `examples/equity_cli.py`.

Run it from the repository root with:

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
As  Ah  Kd  Tc  7s
```

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
│   │   └── fast_evaluator.py
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
│   └── benchmark.py
│
└── README.md
```

## Hand Evaluation

Poker_Sim contains two hand evaluators.

### Reference Evaluator

`evaluator.py` prioritizes readability and correctness.

Hands are evaluated into comparable tuples representing:

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

### Optimized Evaluator

`fast_evaluator.py` uses a lookup-table-based approach to reduce repeated branching and improve evaluation speed.

The optimized evaluator is checked against the reference evaluator using deterministic tests and randomized hand comparisons.

## Equity Simulation

### Hero vs Random Opponent

```python
simulator.simulate_equity(
    hero,
    num_random_opponents=1,
    num_trials=100000
)
```

### Hero vs Known Opponent

```python
simulator.simulate_equity(
    hero,
    known_opponent_hands=[villain],
    num_trials=100000
)
```

### Hero vs Range

```python
simulator.simulate_equity_vs_range(
    hero,
    "QQ+, AQs+, AKo",
    known_board=board,
    num_trials=100000
)
```

For hand-vs-range simulation, each trial:

1. Expands the opponent range into legal physical combinations
2. Removes blocked combinations
3. Samples an opponent hand
4. Removes all known cards from the deck
5. Completes the board
6. Evaluates the showdown
7. Records a win, tie, or loss

## Exact Enumeration

Monte Carlo simulation is used when the number of possible outcomes is large.

When the remaining search space is sufficiently small, Poker_Sim automatically switches to exact enumeration.

This allows the engine to produce exact results when enumeration is practical while retaining Monte Carlo simulation for larger game states.

## Testing

Poker_Sim currently contains **62 automated tests**.

The test suite covers:

- Every major poker hand category
- Wheel straights and straight flushes
- Hand-ranking ordering
- Reference vs optimized evaluator consistency
- Randomized evaluator comparisons
- Deck preparation
- Board completion
- Multi-opponent dealing
- Win, tie, and loss scoring
- Exact-solver integration
- Monte Carlo simulation
- Range parsing
- Plus notation
- Interval notation
- Duplicate range handling
- Invalid range detection
- Blocker handling
- Hand-vs-range simulation
- Guaranteed win, loss, and tie scenarios

Run the complete suite with:

```bash
python3 -m pytest -v
```

## Performance

Poker_Sim includes a benchmark comparing the branching reference evaluator against the optimized lookup-table evaluator.

### 200,000-Hand Benchmark

| Hand Size | Reference Evaluator | Lookup Evaluator | Speedup |
|---|---:|---:|---:|
| 5-card | 194,663 hands/sec | 1,630,811 hands/sec | 8.38x |
| 6-card | 184,340 hands/sec | 570,576 hands/sec | 3.10x |
| 7-card | 184,640 hands/sec | 221,324 hands/sec | 1.20x |

### 1,000,000-Hand Benchmark

| Hand Size | Reference Evaluator | Lookup Evaluator | Speedup |
|---|---:|---:|---:|
| 5-card | 188,904 hands/sec | 1,421,199 hands/sec | 7.52x |
| 6-card | 182,925 hands/sec | 572,677 hands/sec | 3.13x |
| 7-card | 182,167 hands/sec | 217,746 hands/sec | 1.20x |

The largest observed speedup was approximately **8.4x**, with the lookup evaluator exceeding **1.6 million 5-card hand evaluations per second**.

Run the benchmark with:

```bash
python3 -m benchmarks.benchmark
```

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

Install test dependencies:

```bash
pip install pytest
```

Run the test suite:

```bash
python3 -m pytest -v
```

## Design

The engine is divided into separate layers:

```text
Cards / Deck
      ↓
Hand Construction
      ↓
Hand Evaluation
      ↓
Exact / Monte Carlo Simulation
      ↓
Range Parsing + Blockers
      ↓
Equity Analysis
```

The separation between the reference and optimized evaluators also provides an independent way to validate the performance-oriented implementation.

## Roadmap

The core simulation and range-analysis backend is complete.

Planned additions include:

- Improved command-line interface
- Web-based equity calculator
- REST API
- Weighted opponent ranges
- Range-vs-range analysis
- Equity visualization
- Automated poker agent for simulation and permitted competition environments

## Author

**Aryan Moore**  
Computer Science, Princeton University
