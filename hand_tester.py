from evaluator import (
    isStraight, isFlush, isStraightFlush,
    isFourOfAKind, isFullHouse, isThreeOfAKind, isTwoPair, isOnePair, isHighCard,
    evaluate_hand,
)
import cards


def h(*card_specs):
    """
    Build a hand from (suit, rank) pairs, sorted ascending -- exactly what
    hand.make_hand() produces in real usage. isStraightFlush() in
    particular relies on the hand being sorted, so tests should always
    go through this rather than listing raw card ints out of order.
    """
    return sorted(suit * 13 + rank for suit, rank in card_specs)


def test_straight():
    # 2-3-4-5-6 of Spades
    assert isStraight(h((0, 0), (0, 1), (0, 2), (0, 3), (0, 4))) == [5, 6]

    # 2-3-4-5-6, mixed suits
    assert isStraight(h((0, 0), (1, 1), (2, 2), (3, 3), (0, 4))) == [5, 6]

    # Duplicate rank shouldn't matter
    assert isStraight(h((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4))) == [5, 6]

    # Not a straight
    assert isStraight(h((0, 0), (0, 1), (0, 2), (0, 5), (0, 6))) is False

    # Wheel: A-2-3-4-5, mixed suits -- Ace is now raw rank 12, not 0
    assert isStraight(h((0, 12), (1, 0), (2, 1), (3, 2), (0, 3))) == [5, 5]

    # Broadway: 10-J-Q-K-A, mixed suits
    assert isStraight(h((0, 8), (1, 9), (2, 10), (3, 11), (0, 12))) == [5, 14]

    print("\u2713 Straight tests passed")


def test_flush():
    # Five Spades: 2,4,6,8,10
    assert isFlush(h((0, 0), (0, 2), (0, 4), (0, 6), (0, 8))) == [6, 10, 8, 6, 4, 2]

    # Six Spades: 2,4,6,8,10,Q -- lowest kicker (2) gets dropped, only top 5 count
    assert isFlush(h((0, 0), (0, 2), (0, 4), (0, 6), (0, 8), (0, 10))) == [6, 12, 10, 8, 6, 4]

    # Ace-high flush: confirms Ace sorts as the top kicker, not the bottom
    assert isFlush(h((0, 12), (0, 1), (0, 3), (0, 5), (0, 7))) == [6, 14, 9, 7, 5, 3]

    # Not a flush: no suit has 5+
    assert isFlush(h((0, 0), (1, 0), (2, 0), (3, 0), (0, 5))) is False

    print("\u2713 Flush tests passed")


def test_straight_flush():
    # 2-6 of Spades
    assert isStraightFlush(h((0, 0), (0, 1), (0, 2), (0, 3), (0, 4))) == [9, 6]

    # 3-7 of Spades
    assert isStraightFlush(h((0, 1), (0, 2), (0, 3), (0, 4), (0, 5))) == [9, 7]

    # Wheel straight flush: A-2-3-4-5 of Hearts
    assert isStraightFlush(h((1, 12), (1, 0), (1, 1), (1, 2), (1, 3))) == [9, 5]

    # Royal / Broadway straight flush: 10-J-Q-K-A of Diamonds
    assert isStraightFlush(h((2, 8), (2, 9), (2, 10), (2, 11), (2, 12))) == [9, 14]

    # A genuinely higher straight flush should win over an overlapping wheel
    # in the same suit (2-3-4-5-6 of Spades beats the A-2-3-4-5 wheel also present)
    assert isStraightFlush(h((0, 12), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4))) == [9, 6]

    # Straight, but not a flush (mixed suits)
    assert isStraightFlush(h((0, 0), (1, 1), (2, 2), (3, 3), (0, 4))) is False

    # Flush, but not a straight (gaps in rank)
    assert isStraightFlush(h((0, 0), (0, 2), (0, 4), (0, 6), (0, 8))) is False

    print("\u2713 Straight flush tests passed")


def test_four_of_a_kind():
    # Quad Kings + Ace kicker -- specifically checks the kicker bug we
    # already caught once (raw-rank iteration order != strength order)
    assert isFourOfAKind(h((0, 11), (1, 11), (2, 11), (3, 11), (0, 12))) == [8, 13, 14]

    # Quad Aces + King kicker
    assert isFourOfAKind(h((0, 12), (1, 12), (2, 12), (3, 12), (0, 11))) == [8, 14, 13]

    # Quad low cards + low kicker
    assert isFourOfAKind(h((0, 0), (1, 0), (2, 0), (3, 0), (0, 1))) == [8, 2, 3]

    # No quads -- just trips
    assert isFourOfAKind(h((0, 0), (1, 0), (2, 0), (0, 5), (1, 6))) is False

    print("\u2713 Four of a kind tests passed")


def test_full_house():
    # Trips over a pair
    assert isFullHouse(h((0, 12), (1, 12), (2, 12), (0, 11), (1, 11))) == [7, 14, 13]

    # Trips over a HIGHER pair rank still loses to trip rank -- trips always
    # set the primary tiebreak regardless of the pair's rank
    assert isFullHouse(h((0, 0), (1, 0), (2, 0), (0, 12), (1, 12))) == [7, 2, 14]

    # 7-card hand with two different trips: the second trips' rank
    # becomes the "pair" half of the full house
    assert isFullHouse(h((0, 4), (1, 4), (2, 4), (0, 8), (1, 8), (2, 8), (3, 1))) == [7, 10, 6]

    # Trips + two different pairs -- higher pair should be used
    assert isFullHouse(h((0, 4), (1, 4), (2, 4), (0, 8), (1, 8), (0, 1), (1, 1))) == [7, 6, 10]

    # Just trips, no pair -- not a full house
    assert isFullHouse(h((0, 4), (1, 4), (2, 4), (0, 8), (1, 9))) is False

    # Two pair, no trips -- not a full house
    assert isFullHouse(h((0, 4), (1, 4), (0, 8), (1, 8), (0, 1))) is False

    print("\u2713 Full house tests passed")


def test_three_of_a_kind():
    # Basic trips + 2 kickers
    assert isThreeOfAKind(h((0, 4), (1, 4), (2, 4), (0, 12), (1, 8))) == [4, 6, 14, 10]

    # Trips still detected even alongside a pair (isThreeOfAKind doesn't
    # need to know about full houses -- that's evaluate_hand's job)
    assert isThreeOfAKind(h((0, 4), (1, 4), (2, 4), (0, 8), (1, 8))) == [4, 6, 10]

    # Ace trips
    assert isThreeOfAKind(h((0, 12), (1, 12), (2, 12), (0, 0), (1, 1))) == [4, 14, 3, 2]

    # No trips -- just two pair
    assert isThreeOfAKind(h((0, 4), (1, 4), (0, 8), (1, 8), (0, 1))) is False

    print("\u2713 Three of a kind tests passed")


def test_two_pair():
    # Aces and Kings with a kicker
    assert isTwoPair(h((0, 12), (1, 12), (0, 11), (1, 11), (0, 3))) == [3, 14, 13, 5]

    # 7-card hand with THREE pairs: top two pairs count, third pair's rank
    # becomes the kicker
    assert isTwoPair(h((0, 12), (1, 12), (0, 11), (1, 11), (0, 3), (1, 3), (2, 0))) == [3, 14, 13, 5]

    # Low pairs with an Ace kicker -- confirms Ace sorts as top kicker,
    # not bottom
    assert isTwoPair(h((0, 1), (1, 1), (0, 3), (1, 3), (0, 12))) == [3, 5, 3, 14]

    # Only one pair -- not two pair
    assert isTwoPair(h((0, 4), (1, 4), (0, 8), (1, 9), (2, 1))) is False

    print("\u2713 Two pair tests passed")


def test_one_pair():
    # Basic pair of Aces + 3 kickers
    assert isOnePair(h((0, 12), (1, 12), (0, 4), (1, 8), (2, 1))) == [2, 14, 10, 6, 3]

    # Low pair with an Ace kicker -- Ace should be the first (highest) kicker
    assert isOnePair(h((0, 1), (1, 1), (0, 12), (1, 8), (2, 4))) == [2, 3, 14, 10, 6]

    # 7-card hand, only one pair among the rest
    assert isOnePair(h((0, 4), (1, 4), (0, 0), (1, 8), (2, 1), (3, 10), (0, 6))) == [2, 6, 12, 10, 8]

    # No pair at all
    assert isOnePair(h((0, 0), (1, 3), (2, 6), (3, 9), (0, 12))) is False

    print("\u2713 One pair tests passed")


def test_high_card():
    # Ace-high, no pairs -- confirms Ace sorts to the front
    assert isHighCard(h((0, 12), (1, 3), (2, 6), (3, 9), (0, 1))) == [1, 14, 11, 8, 5, 3]

    # 7 cards, only the top 5 count
    assert isHighCard(h((0, 12), (1, 10), (2, 8), (3, 6), (0, 4), (1, 2), (2, 0))) == [1, 14, 12, 10, 8, 6]

    print("\u2713 High card tests passed")


def test_evaluate_hand_ordering():
    # Sanity-check the full ranking ladder by comparing evaluate_hand()
    # output across categories directly with > -- this is the comparison
    # style the whole tuple-based design is meant to support.
    straight_flush = evaluate_hand(h((0, 0), (0, 1), (0, 2), (0, 3), (0, 4)))
    quads = evaluate_hand(h((0, 12), (1, 12), (2, 12), (3, 12), (0, 0)))
    full_house = evaluate_hand(h((0, 12), (1, 12), (2, 12), (0, 11), (1, 11)))
    flush = evaluate_hand(h((0, 12), (0, 1), (0, 3), (0, 5), (0, 7)))
    straight = evaluate_hand(h((0, 0), (1, 1), (2, 2), (3, 3), (0, 4)))
    trips = evaluate_hand(h((0, 4), (1, 4), (2, 4), (0, 8), (1, 9)))
    two_pair = evaluate_hand(h((0, 12), (1, 12), (0, 11), (1, 11), (0, 3)))
    one_pair = evaluate_hand(h((0, 12), (1, 12), (0, 4), (1, 8), (2, 1)))
    high_card = evaluate_hand(h((0, 12), (1, 3), (2, 6), (3, 9), (0, 1)))

    ladder = [high_card, one_pair, two_pair, trips, straight, flush, full_house, quads, straight_flush]
    for weaker, stronger in zip(ladder, ladder[1:]):
        assert stronger > weaker, f"{stronger} should outrank {weaker}"

    print("\u2713 Evaluate_hand category ordering passed")


if __name__ == "__main__":
    test_straight()
    test_flush()
    test_straight_flush()
    test_four_of_a_kind()
    test_full_house()
    test_three_of_a_kind()
    test_two_pair()
    test_one_pair()
    test_high_card()
    test_evaluate_hand_ordering()

    print("\nAll tests passed!")