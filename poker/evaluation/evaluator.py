from poker import cards

# Category numbers, low to high. Royal Flush isn't a separate category --
# it's just a Straight Flush whose high tiebreak value is Ace (14).
HIGH_CARD = 1
ONE_PAIR = 2
TWO_PAIR = 3
THREE_OF_A_KIND = 4
STRAIGHT = 5
FLUSH = 6
FULL_HOUSE = 7
FOUR_OF_A_KIND = 8
STRAIGHT_FLUSH = 9


def strength(rank):
    """
    Convert cards.py's rank encoding (2=0, 3=1, ..., K=11, A=12) into a
    human-scale comparison value (2=2, ..., K=13, A=14).

    This is now a trivial, branchless +2 -- unlike the old A=0 encoding,
    raw rank order already matches strength order for every card, Ace
    included, so no special-casing is needed anywhere kickers, pairs,
    trips, or quads are compared. That was the whole point of moving
    Ace to the high end.
    """
    return rank + 2


def rank_counts(a_hand):
    """counts[r] = how many cards of raw rank r (0="2"..12=A) are in the hand."""
    counts = bytearray(13)
    for card in a_hand:
        counts[card % 13] += 1
    return counts


def find_straight_high(ranks):
    """
    ranks: iterable of raw ranks (0="2"..12=A).
    Returns the strength of the highest straight, or None.

    Bitmask approach, mirrored from the old A=0 version: with Ace now the
    HIGH card, Broadway (10-J-Q-K-A, raw ranks 8-12) is naturally
    consecutive and needs no help. The wheel (A-2-3-4-5) is the one that
    now needs a hand -- so Ace (bit 12) is echoed at a virtual "position
    0" (one below raw rank 0) so it can also complete a low straight,
    while everything else just slides a 5-bit window and checks for a
    match, no set-building or sorting required.
    """
    bits = 0
    for r in ranks:
        bits |= 1 << (r + 1)  # shift all raw ranks up one, to positions 1..13
    if bits & (1 << 13):      # Ace present (raw rank 12, now at position 13)
        bits |= 1 << 0        # echo Ace at virtual position 0, for the wheel

    if bin(bits).count("1") < 5:
        return None  # can't have 5 in a row without 5 distinct ranks present

    for start in range(9, -1, -1):
        window = 0b11111 << start
        if bits & window == window:
            top_position = start + 4
            top_raw_rank = top_position - 1  # undo the +1 shift; always >= 0
            return strength(top_raw_rank)
    return None


def isStraightFlush(a_hand):
    """
    Fast path: a_hand is sorted ascending and all card ints are unique
    (guaranteed by hand.make_hand + a standard deck), so if
    a_hand[i] + k == a_hand[i+k], those k+1 cards MUST be k+1 consecutive
    integers -- no need to check the cards in between individually.

    Same suit + consecutive card ints == consecutive ranks, since suit is
    the high bits (card = suit*13 + rank). With Ace now the highest raw
    rank (12), Broadway (10-J-Q-K-A, raw ranks 8-12) falls straight out of
    the general consecutive-integers check below -- no special case
    needed. The wheel (A-2-3-4-5) is the one exception now: raw ranks
    0-3 (2,3,4,5) are consecutive integers, but Ace (raw rank 12) sits
    far above them, so it's checked separately.

    The general check is tried first at each index: if a hand happens to
    contain both a wheel (ranks 0-3 + Ace) AND a genuinely higher
    straight flush starting at the same index (e.g. ranks 0-4, no Ace
    needed), the general/higher one must win, so it can't be skipped in
    favor of the wheel check.
    """
    n = len(a_hand)
    for i in range(n - 4, -1, -1):
        if i + 4 < n and a_hand[i] + 4 == a_hand[i + 4] and a_hand[i] // 13 == a_hand[i + 4] // 13:
            return [STRAIGHT_FLUSH, strength(a_hand[i + 4] % 13)]
        if (a_hand[i] + 3 == a_hand[i + 3] and a_hand[i] // 13 == a_hand[i + 3] // 13
                and a_hand[i] % 13 == 0 and a_hand[i] + 12 in a_hand):
            return [STRAIGHT_FLUSH, 5]  # Wheel straight flush, 5 high
    return False


def _four_of_a_kind_from_counts(counts):
    quad_rank = None
    for r in range(13):
        if counts[r] == 4:
            quad_rank = r
            break  # at most one rank can have count 4 in a real hand
    if quad_rank is None:
        return False

    kicker_rank = -1
    for r in range(13):
        if r != quad_rank and counts[r] > 0 and r > kicker_rank:
            kicker_rank = r
    return [FOUR_OF_A_KIND, strength(quad_rank), strength(kicker_rank)]


def _full_house_from_counts(counts):
    trips = sorted((r for r in range(13) if counts[r] >= 3), reverse=True)
    if not trips:
        return False

    pairs = sorted((r for r in range(13) if counts[r] >= 2), reverse=True)

    trip_rank = trips[0]
    pair_candidates = [trips[1]] if len(trips) > 1 else []
    pair_candidates += [r for r in pairs if r != trip_rank and r not in pair_candidates]

    if not pair_candidates:
        return False
    return [FULL_HOUSE, strength(trip_rank), strength(pair_candidates[0])]


def _flush_from_hand(a_hand, suit_counts):
    flush_suit = None
    for s in range(4):
        if suit_counts[s] >= 5:
            flush_suit = s
            break
    if flush_suit is None:
        return False

    ranks = sorted((c % 13 for c in a_hand if c // 13 == flush_suit), reverse=True)[:5]
    return [FLUSH] + [strength(r) for r in ranks]


def _three_of_a_kind_from_counts(counts):
    trips = [r for r in range(13) if counts[r] == 3]
    if not trips:
        return False
    trip_rank = max(trips)
    kickers = sorted((r for r in range(13) if r != trip_rank and counts[r] > 0), reverse=True)[:2]
    return [THREE_OF_A_KIND, strength(trip_rank)] + [strength(r) for r in kickers]


def _two_pair_from_counts(counts):
    pairs = sorted((r for r in range(13) if counts[r] >= 2), reverse=True)
    if len(pairs) < 2:
        return False
    top_two = pairs[:2]
    kicker_rank = -1
    for r in range(13):
        if r not in top_two and counts[r] > 0 and r > kicker_rank:
            kicker_rank = r
    kicker = strength(kicker_rank) if kicker_rank != -1 else 0
    return [TWO_PAIR, strength(top_two[0]), strength(top_two[1]), kicker]


def _one_pair_from_counts(counts):
    pairs = [r for r in range(13) if counts[r] == 2]
    if not pairs:
        return False
    pair_rank = max(pairs)
    kickers = sorted((r for r in range(13) if r != pair_rank and counts[r] > 0), reverse=True)[:3]
    return [ONE_PAIR, strength(pair_rank)] + [strength(r) for r in kickers]


# Public isX() wrappers -- each computes its own counts, useful for testing
# a single category in isolation. evaluate_hand() below skips these and
# computes counts/suit_counts exactly once for the whole hand instead.

def isFourOfAKind(a_hand):
    return _four_of_a_kind_from_counts(rank_counts(a_hand))


def isFullHouse(a_hand):
    return _full_house_from_counts(rank_counts(a_hand))


def isFlush(a_hand):
    suit_counts = [0, 0, 0, 0]
    for c in a_hand:
        suit_counts[c // 13] += 1
    return _flush_from_hand(a_hand, suit_counts)


def isStraight(a_hand):
    ranks = [c % 13 for c in a_hand]
    high = find_straight_high(ranks)
    if high is None:
        return False
    return [STRAIGHT, high]


def isThreeOfAKind(a_hand):
    return _three_of_a_kind_from_counts(rank_counts(a_hand))


def isTwoPair(a_hand):
    return _two_pair_from_counts(rank_counts(a_hand))


def isOnePair(a_hand):
    return _one_pair_from_counts(rank_counts(a_hand))


def isHighCard(a_hand):
    ranks = sorted((c % 13 for c in a_hand), reverse=True)[:5]
    return [HIGH_CARD] + [strength(r) for r in ranks]


def evaluate_hand(a_hand):
    """
    Return the best [category, *tiebreaks] list for this hand
    (2-7+ cards, e.g. hole cards + community cards).

    Since every isX() returns a list starting with its category number,
    and higher categories/tiebreaks always sort higher, you can compare
    two hands directly: evaluate_hand(a) > evaluate_hand(b)
    """
    counts = rank_counts(a_hand)

    suit_counts = [0, 0, 0, 0]
    for card in a_hand:
        suit_counts[card // 13] += 1
    has_flush_suit = suit_counts[0] >= 5 or suit_counts[1] >= 5 or suit_counts[2] >= 5 or suit_counts[3] >= 5

    if has_flush_suit:
        sf = isStraightFlush(a_hand)
        if sf:
            return sf

    quad = _four_of_a_kind_from_counts(counts)
    if quad:
        return quad

    fh = _full_house_from_counts(counts)
    if fh:
        return fh

    if has_flush_suit:
        fl = _flush_from_hand(a_hand, suit_counts)
        if fl:
            return fl

    ranks = [c % 13 for c in a_hand]
    straight_high = find_straight_high(ranks)
    if straight_high is not None:
        return [STRAIGHT, straight_high]

    tk = _three_of_a_kind_from_counts(counts)
    if tk:
        return tk

    tp = _two_pair_from_counts(counts)
    if tp:
        return tp

    op = _one_pair_from_counts(counts)
    if op:
        return op

    top5 = sorted(ranks, reverse=True)[:5]
    return [HIGH_CARD] + [strength(r) for r in top5]