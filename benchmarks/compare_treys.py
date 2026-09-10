import random
import time
from statistics import median

from treys import Card, Evaluator

from poker.evaluation.evaluator import evaluate_hand as branching_evaluate
from poker.evaluation.fast_evaluator import evaluate_hand as fast_evaluate


NUM_HANDS = 1_000_000
NUM_TRIALS = 5
SEED = 42


def generate_5_card_hands(n):
    rng = random.Random(SEED)
    deck = list(range(52))

    return [rng.sample(deck, 5) for _ in range(n)]


def to_treys_card(card_int):
    """
    Convert Poker_Sim integer encoding to Treys encoding.

    Poker_Sim:
      ranks 2..A -> 0..12
      suits:
        0 = Spades
        1 = Hearts
        2 = Diamonds
        3 = Clubs
    """

    rank_index = card_int % 13
    suit_index = card_int // 13

    rank_chars = "23456789TJQKA"
    suit_chars = "shdc"

    return Card.new(rank_chars[rank_index] + suit_chars[suit_index])


def convert_hands_for_treys(hands):
    """
    Convert all cards BEFORE benchmarking Treys so card conversion
    is not included in Treys evaluation time.
    """
    converted = []

    for hand in hands:
        cards = [to_treys_card(card) for card in hand]

        hole = cards[:2]
        board = cards[2:]

        converted.append((hole, board))

    return converted


def branching_wrapper(hand):
    return branching_evaluate(hand)


def fast_wrapper(hand):
    return fast_evaluate(hand)


def benchmark(name, fn, hands, trials=NUM_TRIALS):
    rates = []

    print(name)

    # Warmup
    for hand in hands[:10_000]:
        fn(hand)

    for trial in range(1, trials + 1):
        start = time.perf_counter()

        result = None
        for hand in hands:
            result = fn(hand)

        elapsed = time.perf_counter() - start
        rate = len(hands) / elapsed
        rates.append(rate)

        print(
            f"  Trial {trial}: "
            f"{elapsed:.4f} sec | "
            f"{rate:,.0f} evals/sec"
        )

    median_rate = median(rates)

    print(f"  Median: {median_rate:,.0f} evals/sec")
    print(f"  Last result: {result}")
    print()

    return median_rate


def benchmark_treys(treys_hands, trials=NUM_TRIALS):
    evaluator = Evaluator()
    rates = []

    print("Treys")

    for trial in range(1, trials + 1):
        start = time.perf_counter()

        checksum = 0

        for hole, board in treys_hands:
            result = evaluator.evaluate(board, hole)
            checksum ^= result

        elapsed = time.perf_counter() - start
        rate = len(treys_hands) / elapsed
        rates.append(rate)

        print(
            f"  Trial {trial}: "
            f"{elapsed:.4f} sec | "
            f"{rate:,.0f} evals/sec"
        )

    median_rate = median(rates)

    print(f"  Median:  {median_rate:,.0f} evals/sec")
    print(f"  Checksum: {checksum}")
    print()

    return median_rate


def main():
    print("=" * 60)
    print("Poker Evaluator Benchmark")
    print("=" * 60)
    print()

    print(f"Generating {NUM_HANDS:,} random 5-card hands...")
    hands = generate_5_card_hands(NUM_HANDS)
    print("Done.")
    print()

    print("Pre-converting hands for Treys...")
    treys_hands = convert_hands_for_treys(hands)
    print("Done.")
    print()

    branching_rate = benchmark(
        "Branching evaluator",
        branching_wrapper,
        hands,
    )

    fast_rate = benchmark(
        "Fast evaluator",
        fast_wrapper,
        hands,
    )

    treys_rate = benchmark_treys(treys_hands)

    print("=" * 60)
    print("Relative Performance")
    print("=" * 60)

    print(
        f"Fast vs branching: "
        f"{fast_rate / branching_rate:.2f}x"
    )

    print(
        f"Fast vs Treys:     "
        f"{fast_rate / treys_rate:.2f}x"
    )

    print()
    print("Median Throughput")
    print("-" * 60)
    print(f"Branching: {branching_rate:,.0f} evals/sec")
    print(f"Fast:      {fast_rate:,.0f} evals/sec")
    print(f"Treys:     {treys_rate:,.0f} evals/sec")


if __name__ == "__main__":
    main()