"""
Lookup-table hand evaluator (Cactus Kev style), built on top of evaluator.py's
category constants and strength()/find_straight_high() so results are
identical to evaluator.evaluate_hand() -- just much faster to compute.

Core idea: assign each rank a distinct prime number. The product of a
5-card hand's rank-primes is a perfect hash of the hand's rank *multiset*
(two hands with the same ranks-with-repeats produce the same product,
and no other combination collides, since prime factorization is unique).

So: precompute every possible 5-rank multiset's category+tiebreak ONCE at
import time (there are only 6188 of them, filtering out impossible ones
where a single rank appears 5 times), store it in a dict keyed by prime
product, split into a flush table and a non-flush table (since the same
5 ranks can be either a flush or not, depending on suits).

Evaluating a hand then costs: one multiply loop to build the product,
one suit check, and one dict lookup. No branching over hand categories,
no per-hand sorting.

For 7-card hands (hole cards + board), we check the best of all 21
5-card combinations. That's 21 dict lookups -- still far cheaper than
1 call to a branching evaluator.
"""

import itertools
from poker.evaluation.evaluator import (
    strength, find_straight_high,
    HIGH_CARD, ONE_PAIR, TWO_PAIR, THREE_OF_A_KIND, STRAIGHT,
    FLUSH, FULL_HOUSE, FOUR_OF_A_KIND, STRAIGHT_FLUSH,
)

# One prime per rank (0="2", 1="3", ..., 12="A", per cards.py's current
# encoding). Values themselves don't matter, only that they're distinct
# primes -- used purely for the unique-product trick.
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def _prime_product(ranks):
    product = 1
    for r in ranks:
        product *= PRIMES[r]
    return product


def _categorize_5ranks(ranks, is_flush):
    """
    ranks: exactly 5 raw ranks (0="2"..12="A"), with repeats allowed unless
    is_flush (a flush by definition has 5 distinct ranks, since you can't
    hold two cards of the same rank and same suit).
    Returns a (category, *tiebreaks) tuple, matching evaluator.py's shape.
    """
    counts = [0] * 13
    for r in ranks:
        counts[r] += 1

    distinct = sorted(set(ranks))
    straight_high = find_straight_high(ranks) if len(distinct) == 5 else None

    if is_flush:
        if straight_high:
            return (STRAIGHT_FLUSH, straight_high)
        strengths_desc = sorted((strength(r) for r in ranks), reverse=True)
        return tuple([FLUSH] + strengths_desc)

    quad = next((r for r in range(13) if counts[r] == 4), None)
    if quad is not None:
        kicker = max(strength(r) for r in range(13) if r != quad and counts[r] > 0)
        return (FOUR_OF_A_KIND, strength(quad), kicker)

    trips = sorted((r for r in range(13) if counts[r] == 3), key=strength, reverse=True)
    pairs = sorted((r for r in range(13) if counts[r] == 2), key=strength, reverse=True)

    if trips and pairs:
        return (FULL_HOUSE, strength(trips[0]), strength(pairs[0]))

    if straight_high:
        return (STRAIGHT, straight_high)

    if trips:
        kickers = sorted(
            (strength(r) for r in range(13) if r != trips[0] and counts[r] > 0),
            reverse=True,
        )
        return tuple([THREE_OF_A_KIND, strength(trips[0])] + kickers)

    if len(pairs) >= 2:
        top2 = pairs[:2]
        kicker = max(strength(r) for r in range(13) if r not in top2 and counts[r] > 0)
        return (TWO_PAIR, strength(top2[0]), strength(top2[1]), kicker)

    if len(pairs) == 1:
        kickers = sorted(
            (strength(r) for r in range(13) if r != pairs[0] and counts[r] > 0),
            reverse=True,
        )
        return tuple([ONE_PAIR, strength(pairs[0])] + kickers)

    strengths_desc = sorted((strength(r) for r in ranks), reverse=True)
    return tuple([HIGH_CARD] + strengths_desc)


def _build_tables():
    nonflush = {}
    flush = {}
    for ranks in itertools.combinations_with_replacement(range(13), 5):
        counts = {}
        for r in ranks:
            counts[r] = counts.get(r, 0) + 1
        if any(c > 4 for c in counts.values()):
            continue  # impossible with only 4 suits

        product = _prime_product(ranks)
        nonflush[product] = _categorize_5ranks(list(ranks), is_flush=False)
        if len(set(ranks)) == 5:
            flush[product] = _categorize_5ranks(list(ranks), is_flush=True)
    return nonflush, flush


# Built once at import time -- 6188 rank-multisets, trivially fast.
_NONFLUSH_TABLE, _FLUSH_TABLE = _build_tables()


def evaluate_5(card5):
    """Evaluate an exact 5-card hand. card5: any iterable of 5 card ints."""
    c0, c1, c2, c3, c4 = card5
    product = (PRIMES[c0 % 13] * PRIMES[c1 % 13] * PRIMES[c2 % 13]
               * PRIMES[c3 % 13] * PRIMES[c4 % 13])
    if (c0 // 13) == (c1 // 13) == (c2 // 13) == (c3 // 13) == (c4 // 13):
        return _FLUSH_TABLE[product]
    return _NONFLUSH_TABLE[product]


# All C(7,5) = 21 index combinations, precomputed once so evaluate_hand()
# doesn't call itertools.combinations per hand.
_COMBOS_7 = list(itertools.combinations(range(7), 5))
_COMBOS_6 = list(itertools.combinations(range(6), 5))


def evaluate_hand(a_hand):
    """
    Drop-in replacement for evaluator.evaluate_hand(), same return shape.
    Handles 5, 6, or 7 card hands (hole cards + up to 5 board cards).

    Inlined rather than calling evaluate_5() per combo: Python function-call
    overhead dominates at this scale, so for 6/7-card hands we compute
    ranks/suits/rank-primes exactly once, then loop over the 21 (or 6)
    precomputed index-combinations doing only integer multiplies, suit
    comparisons, and dict lookups -- no further function calls.
    """
    # Local aliases: local variable access is faster than global lookup
    # in a hot loop.
    primes = PRIMES
    nonflush = _NONFLUSH_TABLE
    flush = _FLUSH_TABLE

    n = len(a_hand)
    ranks = [c % 13 for c in a_hand]
    suits = [c // 13 for c in a_hand]
    rank_primes = [primes[r] for r in ranks]

    if n == 5:
        product = rank_primes[0] * rank_primes[1] * rank_primes[2] * rank_primes[3] * rank_primes[4]
        if suits[0] == suits[1] == suits[2] == suits[3] == suits[4]:
            return flush[product]
        return nonflush[product]

    if n == 6:
        combos = _COMBOS_6
    elif n == 7:
        combos = _COMBOS_7
    else:
        combos = itertools.combinations(range(n), 5)

    best = None
    for i0, i1, i2, i3, i4 in combos:
        product = rank_primes[i0] * rank_primes[i1] * rank_primes[i2] * rank_primes[i3] * rank_primes[i4]
        if suits[i0] == suits[i1] == suits[i2] == suits[i3] == suits[i4]:
            result = flush[product]
        else:
            result = nonflush[product]
        if best is None or result > best:
            best = result
    return best