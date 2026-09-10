from itertools import combinations

from poker.evaluation.fast_evaluator import (
    PRIMES,
    _NONFLUSH_TABLE,
    _FLUSH_TABLE,
)

from poker.evaluation.evaluator import(
    STRAIGHT_FLUSH,
    FOUR_OF_A_KIND,
    FULL_HOUSE,
    FLUSH,
    STRAIGHT,
    THREE_OF_A_KIND,
    TWO_PAIR,
    ONE_PAIR,
    HIGH_CARD,
)

CARD_RANK = tuple(c % 13 for c in range(52))
CARD_PRIME = tuple(PRIMES[c % 13] for c in range(52))
CARD_SUIT = tuple(c // 13 for c in range(52))
COMBOS_6 = tuple(combinations(range(6), 5))
COMBOS_7 = tuple(combinations(range(7), 5))
STRAIGHT_MASKS = tuple(0b11111 << i for i in range(8,-1,-1)) + (0b1000000001111,)
FLUSH_BY_MASK = [None] * 8192

for mask in range(8192):
    if mask.bit_count() >= 5:
        top = []

        for rank in range(12, -1, -1):
            if mask & (1 << rank):
                top.append(rank + 2)

                if len(top) == 5:
                    break

        FLUSH_BY_MASK[mask] = (FLUSH, *top)

FLUSH_BY_MASK = tuple(FLUSH_BY_MASK)
STRAIGHT_HIGH_BY_MASK = [0] * 8192

for mask in range(8192):
    for i, straight_mask in enumerate(STRAIGHT_MASKS):
        if (mask & straight_mask) == straight_mask:
            STRAIGHT_HIGH_BY_MASK[mask] = 14 - i
            break

STRAIGHT_HIGH_BY_MASK = tuple(STRAIGHT_HIGH_BY_MASK)
TOP2_BY_MASK = [None] * 8192

for mask in range(8192):
    top = []

    for rank in range(12, -1, -1):
        if mask & (1 << rank):
            top.append(rank + 2)

            if len(top) == 2:
                break

    if len(top) == 2:
        TOP2_BY_MASK[mask] = (top[0], top[1])

TOP2_BY_MASK = tuple(TOP2_BY_MASK)

TOP3_BY_MASK = [None] * 8192

for mask in range(8192):
    top = []

    for rank in range(12, -1, -1):
        if mask & (1 << rank):
            top.append(rank + 2)

            if len(top) == 3:
                break

    if len(top) == 3:
        TOP3_BY_MASK[mask] = (top[0], top[1], top[2])

TOP3_BY_MASK = tuple(TOP3_BY_MASK)

TOP5_BY_MASK = [None] * 8192

for mask in range(8192):
    top = []

    for rank in range(12, -1, -1):
        if mask & (1 << rank):
            top.append(rank + 2)

            if len(top) == 5:
                break

    if len(top) == 5:
        TOP5_BY_MASK[mask] = (top[0], top[1], top[2], top[3], top[4])

TOP5_BY_MASK = tuple(TOP5_BY_MASK)
TOP1_BY_MASK = [None] * 8192

for mask in range(8192):
    for rank in range(12, -1, -1):
        if mask & (1 << rank):
            TOP1_BY_MASK[mask] = rank + 2
            break

TOP1_BY_MASK = tuple(TOP1_BY_MASK)

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

def evaluate_seven(hand):
    rank_counts = [0] * 13
    suit_counts = [0] * 4

    rank_mask = 0
    suit_masks = [0, 0, 0, 0]

    for card in hand:
        rank = CARD_RANK[card]
        suit = CARD_SUIT[card]
        rank_counts[rank] += 1
        suit_counts[suit] += 1

        bit = 1 << rank

        rank_mask |= bit
        suit_masks[suit] |= bit

    #Checking for dat straight flush
    flush_suit = -1
    for suit in range(4):
        if suit_counts[suit] >= 5:
            flush_suit = suit

            high = STRAIGHT_HIGH_BY_MASK[suit_masks[suit]]
            if high:
                return (STRAIGHT_FLUSH, high)

            #Flush, becuase no Quads/Boat cannot exist if flush exists
            return FLUSH_BY_MASK[suit_masks[flush_suit]]

    # QUADS
    for rank in range(12, -1, -1):
        if rank_counts[rank] == 4:
            kicker_mask = rank_mask & ~(1 << rank)
            return (
                FOUR_OF_A_KIND,
                rank + 2,
                TOP1_BY_MASK[kicker_mask],
            )

    #BOAT BABY
    trip_rank = -1
    pair_rank = -1
    pair2_rank = -1
    for rank in range(12, -1, -1):
        if rank_counts[rank] >= 3:
            trip_rank = rank
            break
    for pairrank in range(12, -1, -1):
        if pairrank != trip_rank and rank_counts[pairrank] >= 2:
            if pair_rank == -1:
                pair_rank = pairrank
            elif pair2_rank == -1:
                pair2_rank = pairrank
                break
    
    if trip_rank != -1 and pair_rank != -1:
        return (FULL_HOUSE, trip_rank + 2, pair_rank + 2)

    #STRAIGHT
    high = STRAIGHT_HIGH_BY_MASK[rank_mask]

    if high:
        return (STRAIGHT, high)

    #TRIPS
    if trip_rank != -1:
        kicker_mask = rank_mask & ~(1 << trip_rank)
        k1, k2 = TOP2_BY_MASK[kicker_mask]

        return (
            THREE_OF_A_KIND,
            trip_rank + 2,
            k1,
            k2,
        )

    #One or Two pairs
    if pair_rank != -1:
        if pair2_rank != -1:
            kicker_mask = rank_mask & ~(1 << pair_rank) & ~(1 << pair2_rank)
            kicker = TOP1_BY_MASK[kicker_mask]

            return (
                TWO_PAIR,
                pair_rank + 2,
                pair2_rank + 2,
                kicker,
            )
        else:
            kicker_mask = rank_mask & ~(1 << pair_rank)
            k1, k2, k3 = TOP3_BY_MASK[kicker_mask]

            return (
                ONE_PAIR,
                pair_rank + 2,
                k1,
                k2,
                k3,
            )
    #High card
    c1, c2, c3, c4, c5 = TOP5_BY_MASK[rank_mask]
    return (HIGH_CARD, c1, c2, c3, c4, c5)

    

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
        c0, c1, c2, c3, c4, c5 = hand

        best = _evaluate_5_cards(c1, c2, c3, c4, c5)

        score = _evaluate_5_cards(c0, c2, c3, c4, c5)
        if score > best:
            best = score

        score = _evaluate_5_cards(c0, c1, c3, c4, c5)
        if score > best:
            best = score

        score = _evaluate_5_cards(c0, c1, c2, c4, c5)
        if score > best:
            best = score

        score = _evaluate_5_cards(c0, c1, c2, c3, c5)
        if score > best:
            best = score

        score = _evaluate_5_cards(c0, c1, c2, c3, c4)
        if score > best:
            best = score

        return best

    elif n == 7:
        return evaluate_seven(hand)

    else:
        raise ValueError(f"Invalid hand length: {n}")