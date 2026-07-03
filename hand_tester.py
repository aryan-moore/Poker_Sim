from evaluator import isStraight, isFlush, isStraightFlush


def test_straight():
    # 2♣ 3♣ 4♣ 5♣ 6♣
    assert isStraight([0, 1, 2, 3, 4]) == [5, 4]

    # 2♣ 3♦ 4♥ 5♠ 6♣
    assert isStraight([0, 14, 28, 42, 4]) == [5, 4]

    # Duplicate rank shouldn't matter
    assert isStraight([0, 1, 2, 3, 4, 17]) == [5, 4]

    # Not a straight
    assert isStraight([0, 1, 2, 5, 6]) is False

    print("✓ Straight tests passed")


def test_flush():
    # Five clubs
    assert isFlush([0, 2, 4, 6, 8]) == [6, 8, 6, 4, 2, 0]

    # Six clubs
    assert isFlush([0, 2, 4, 6, 8, 10]) == [6, 10, 8, 6, 4, 2]

    # Not a flush
    assert isFlush([0, 13, 26, 39, 5]) is False

    print("✓ Flush tests passed")


def test_straight_flush():
    # 2♣-6♣
    assert isStraightFlush([0, 1, 2, 3, 4]) == [9, 4]

    # 3♣-7♣
    assert isStraightFlush([1, 2, 3, 4, 5]) == [9, 5]

    # Straight but not flush
    assert isStraightFlush([0, 14, 28, 42, 4]) is False

    # Flush but not straight
    assert isStraightFlush([0, 2, 4, 6, 8]) is False

    print("✓ Straight flush tests passed")


if __name__ == "__main__":
    test_straight()
    test_flush()
    test_straight_flush()

    print("\nAll tests passed!")