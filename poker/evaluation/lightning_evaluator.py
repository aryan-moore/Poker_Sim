from poker.evaluation.fast_evaluator import (
    PRIMES,
    _NONFLUSH_TABLE,
    _FLUSH_TABLE,
)

CARD_PRIME = tuple(PRIMES[c % 13] for c in range(52))
CARD_SUIT = tuple(c // 13 for c in range(52))


def evaluate_5(hand):
    c0, c1, c2, c3, c4 = hand

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