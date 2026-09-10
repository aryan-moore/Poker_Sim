"""
Benchmark the three Poker_Sim evaluators against Treys on random
5-, 6-, and 7-card hands.

Run from the repository root with:

    python3 -m benchmarks.benchmark

The benchmark:
- generates the same random hands for every evaluator
- converts cards to Treys format before timing
- warms up each evaluator
- runs multiple trials
- reports median throughput
"""

import random
import statistics
import time

from poker.evaluation import evaluator
from poker.evaluation import fast_evaluator
from poker.evaluation import lightning_evaluator

from treys import Evaluator as TreysEvaluator

from benchmarks.compare_treys import to_treys_card


DEFAULT_TRIALS = 200_000
REPEATS = 5
WARMUP_HANDS = 10_000


def make_random_hands(n_hands, cards_per_hand, seed=1):
    """
    Generate sorted random Poker_Sim hands.

    Each card is represented using Poker_Sim's integer encoding 0-51.
    """
    rng = random.Random(seed)
    hands = []

    deck52 = list(range(52))

    for _ in range(n_hands):
        hand = rng.sample(deck52, cards_per_hand)
        hand.sort()
        hands.append(hand)

    return hands


def convert_hands_for_treys(hands):
    """
    Convert Poker_Sim card integers into Treys card integers.

    Conversion happens before timing so the benchmark measures evaluator
    performance rather than representation-conversion overhead.
    """
    return [
        [to_treys_card(card) for card in hand]
        for hand in hands
    ]


def bench(fn, hands, repeats=REPEATS, warmup=WARMUP_HANDS):
    """
    Benchmark fn over hands and return the median elapsed time.

    A warmup is performed first so interpreter specialization and caches
    have a chance to stabilize before timing begins.
    """
    warmup_count = min(warmup, len(hands))

    for hand in hands[:warmup_count]:
        fn(hand)

    times = []

    for _ in range(repeats):
        start = time.perf_counter()

        for hand in hands:
            fn(hand)

        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return statistics.median(times)


def run(cards_per_hand, n_hands=DEFAULT_TRIALS):
    """
    Benchmark all evaluators on one hand size.
    """
    print(
        f"\nGenerating {n_hands:,} random "
        f"{cards_per_hand}-card hands..."
    )

    hands = make_random_hands(
        n_hands=n_hands,
        cards_per_hand=cards_per_hand,
        seed=1,
    )

    treys_hands = convert_hands_for_treys(hands)

    treys_evaluator = TreysEvaluator()

    def treys_eval(treys_hand):
        """
        Treys expects board and hole cards separately.

        We use the first two cards as the player's hole cards and the
        remaining cards as the board.

        Total cards:
            5 -> 2 hole + 3 board
            6 -> 2 hole + 4 board
            7 -> 2 hole + 5 board
        """
        hole_cards = treys_hand[:2]
        board = treys_hand[2:]

        return treys_evaluator.evaluate(board, hole_cards)

    print("Benchmarking branching evaluator...")
    t_branching = bench(
        evaluator.evaluate_hand,
        hands,
    )

    print("Benchmarking fast evaluator...")
    t_fast = bench(
        fast_evaluator.evaluate_hand,
        hands,
    )

    print("Benchmarking lightning evaluator...")
    t_lightning = bench(
        lightning_evaluator.evaluate_hand,
        hands,
    )

    print("Benchmarking Treys...")
    t_treys = bench(
        treys_eval,
        treys_hands,
    )

    branching_rate = n_hands / t_branching
    fast_rate = n_hands / t_fast
    lightning_rate = n_hands / t_lightning
    treys_rate = n_hands / t_treys

    print()
    print("=" * 60)
    print(f"{cards_per_hand}-CARD HANDS")
    print("=" * 60)

    print(f"Trials per run: {n_hands:,}")
    print(f"Repeats:        {REPEATS}")
    print()

    print("Median Throughput")
    print("-" * 60)

    print(
        f"Branching:  {branching_rate:>12,.0f} evals/sec"
    )

    print(
        f"Fast:       {fast_rate:>12,.0f} evals/sec"
        f"   ({fast_rate / branching_rate:.2f}x branching)"
    )

    print(
        f"Lightning:  {lightning_rate:>12,.0f} evals/sec"
        f"   ({lightning_rate / branching_rate:.2f}x branching)"
    )

    print(
        f"Treys:      {treys_rate:>12,.0f} evals/sec"
    )

    print()
    print("Relative Performance")
    print("-" * 60)

    print(
        f"Fast vs Treys:       "
        f"{fast_rate / treys_rate:.2f}x"
    )

    print(
        f"Lightning vs Treys:  "
        f"{lightning_rate / treys_rate:.2f}x"
    )

    print(
        f"Lightning vs Fast:   "
        f"{lightning_rate / fast_rate:.2f}x"
    )


def main():
    run(5, 200_000)
    run(6, 200_000)
    run(7, 200_000)


if __name__ == "__main__":
    main()