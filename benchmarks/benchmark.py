"""
Benchmark evaluator.py (restructured branching) vs fast_evaluator.py
(prime-product lookup table) on random hands.

Usage: python3 -m benchmarks.benchmark
"""

import random
import time

from poker.evaluation import evaluator
from poker.evaluation import fast_evaluator


def make_random_hands(n_hands, cards_per_hand, seed=1):
    rng = random.Random(seed)
    hands = []
    for _ in range(n_hands):
        deck52 = list(range(52))
        rng.shuffle(deck52)
        hands.append(sorted(deck52[:cards_per_hand]))
    return hands


def bench(fn, hands):
    t0 = time.perf_counter()
    for h in hands:
        fn(h)
    return time.perf_counter() - t0


def run(cards_per_hand, n_hands=200000):
    hands = make_random_hands(n_hands, cards_per_hand)

    t_branching = bench(evaluator.evaluate_hand, hands)
    t_lookup = bench(fast_evaluator.evaluate_hand, hands)

    print(f"\n{cards_per_hand}-card hands ({n_hands:,} trials):")
    print(f"  branching:    {n_hands / t_branching:>12,.0f} hands/sec")
    print(f"  lookup table: {n_hands / t_lookup:>12,.0f} hands/sec  "
          f"({t_branching / t_lookup:.2f}x)")


if __name__ == "__main__":
    run(5)
    run(5, 1000000)
    run(6)
    run(6, 1000000)
    run(7)
    run(7, 1000000)