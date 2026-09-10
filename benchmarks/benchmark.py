"""
Benchmark evaluator.py (restructured branching) vs fast_evaluator.py
(prime-product lookup table) on random hands.

Usage: python3 -m benchmarks.benchmark
"""

import random
import time

from poker.evaluation import evaluator
from poker.evaluation import fast_evaluator
from poker.evaluation import lightning_evaluator
from treys import Evaluator as TreysEvaluator
from benchmarks.compare_treys import convert_hands_for_treys


def make_random_hands(n_hands, cards_per_hand, seed=1):
    rng = random.Random(seed)
    hands = []
    for _ in range(n_hands):
        deck52 = list(range(52))
        rng.shuffle(deck52)
        hands.append(sorted(deck52[:cards_per_hand]))
    return hands


def bench(fn, hands, repeats=5, warmup=10000):
    # Warm up the interpreter/cache behavior first
    for h in hands[:warmup]:
        fn(h)

    times = []

    for _ in range(repeats):
        t0 = time.perf_counter()

        for h in hands:
            fn(h)

        times.append(time.perf_counter() - t0)

    times.sort()
    return times[len(times) // 2]


def run(cards_per_hand, n_hands=200000):
    hands = make_random_hands(n_hands, cards_per_hand)
    treys_hands = convert_hands_for_treys(hands)
    t_branching = bench(evaluator.evaluate_hand, hands)
    t_lookup = bench(fast_evaluator.evaluate_hand, hands)
    t_lightning = bench(lightning_evaluator.evaluate_hand, hands)
    t_treys = bench(TreysEvaluator().evaluate, treys_hands)
    print(f"\n{cards_per_hand}-card hands ({n_hands:,} trials):")
    print(f"  branching:    {n_hands / t_branching:>12,.0f} hands/sec")
    print(f"  lookup table: {n_hands / t_lookup:>12,.0f} hands/sec  "
          f"({t_branching / t_lookup:.2f}x)")
    print(f"  lightning:    {n_hands / t_lightning:>12,.0f} hands/sec  "
          f"({t_branching / t_lightning:.2f}x)")
    print(f"  treys:        {n_hands / t_treys:>12,.0f} hands/sec  "
          f"({t_branching / t_treys:.2f}x)")


if __name__ == "__main__":
    run(5)
    run(5, 1000000)
    run(6)
    run(6, 1000000)
    run(7)
    run(7, 1000000)