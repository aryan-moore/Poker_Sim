from itertools import combinations

from poker.evaluation.fast_evaluator import (
    PRIMES,
    _NONFLUSH_TABLE,
    _FLUSH_TABLE,
)

CARD_PRIME = tuple(PRIMES[c % 13] for c in range(52))
CARD_SUIT = tuple(c // 13 for c in range(52))
COMBOS_6 = tuple(combinations(range(6), 5))
COMBOS_7 = tuple(combinations(range(7), 5))

def evaluate_5(hand):
    c0, c1, c2, c3, c4 = hand
    return _evaluate_5_cards(c0, c1, c2, c3, c4)

def _evaluate_5_cards(c0, c1, c2, c3, c4):
    product = (
        CARD_PRIME[c0]
        * CARD_PRIME[c1]
        * CARD_PRIME[c2]
        * CARD_PRIME[c3]
        * CARD_PRIME[c4]
    )

    s0 = CARD_SUIT[c0]

    if (
        s0 == CARD_SUIT[c1]
        and s0 == CARD_SUIT[c2]
        and s0 == CARD_SUIT[c3]
        and s0 == CARD_SUIT[c4]
    ):
        return _FLUSH_TABLE[product]

    return _NONFLUSH_TABLE[product]

def evaluate_hand(hand):
    n = len(hand)

    if n == 5:
        card_prime = CARD_PRIME
        card_suit = CARD_SUIT
        nonflush = _NONFLUSH_TABLE
        flush = _FLUSH_TABLE
        c0, c1, c2, c3, c4 = hand

        product = (
            card_prime[c0]
            * card_prime[c1]
            * card_prime[c2]
            * card_prime[c3]
            * card_prime[c4]
        )
        s0 = card_suit[c0]

        if (
            s0 == card_suit[c1]
            and s0 == card_suit[c2]
            and s0 == card_suit[c3]
            and s0 == card_suit[c4]
        ):
            return flush[product]
        return nonflush[product]     

    elif n == 6:
        first = COMBOS_6[0]
        i0, i1, i2, i3, i4 = first

        best = _evaluate_5_cards(
            hand[i0],
            hand[i1],
            hand[i2],
            hand[i3],
            hand[i4],
        )

        for i0, i1, i2, i3, i4 in COMBOS_6[1:]:
            score = _evaluate_5_cards(
                hand[i0],
                hand[i1],
                hand[i2],
                hand[i3],
                hand[i4],
            )
            if score > best:
                best = score
        return best 

    elif n == 7:
        first = COMBOS_7[0]
        i0, i1, i2, i3, i4 = first
        
        best = _evaluate_5_cards(
            hand[i0],
            hand[i1],
            hand[i2],
            hand[i3],
            hand[i4],
            )
        
        for i0, i1, i2, i3, i4 in COMBOS_7[1:]:
            score = _evaluate_5_cards(
                hand[i0],
                hand[i1],
                hand[i2],
                hand[i3],
                hand[i4],
            )
            if score > best:
                best = score
        return best 

    else:
        raise ValueError(f"Invalid hand length: {n}")