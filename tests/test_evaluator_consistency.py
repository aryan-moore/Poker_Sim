from poker.evaluation import evaluator
from poker.evaluation import fast_evaluator
from poker import deck
from poker import hand
from poker import cards

"""
Test consistency between the two evaluators. The fast evaluator is
faster, but the pure Python evaluator is easier to read and understand. The two should
produce the same results for all hands, so we can use the pure Python evaluator to verify
the fast evaluator is working correctly.
"""

def check_both_evaluators(hole_cards, board):
    """
    Check that both evaluators return the same result for a given hand and board.
    """
    new_hand = hand.make_hand(hole_cards, board)
    fast_eval = fast_evaluator.evaluate_hand(new_hand)
    pure_eval = evaluator.evaluate_hand(new_hand)
    assert fast_eval == pure_eval, f"Fast evaluator returned {fast_eval}, but pure evaluator returned {pure_eval} for hand {hole_cards} and board {board}"

def check_expected_evaluation(hole_cards, board, expected_result):
    """
    Check that both evaluators return the same result for a given hand and board,
    and that the result matches the expected result.
    """
    new_hand = hand.make_hand(hole_cards, board)
    fast_eval = fast_evaluator.evaluate_hand(new_hand)
    pure_eval = evaluator.evaluate_hand(new_hand)
    assert fast_eval == pure_eval, f"Fast evaluator returned {fast_eval}, but pure evaluator returned {pure_eval} for hand {hole_cards} and board {board}"
    assert fast_eval == expected_result, f"Expected result {expected_result}, but got {fast_eval} for hand {hole_cards} and board {board}"

def test_royal_flush():
    hole_cards = cards.make_cards([
        "A of Spades",
        "K of Spades"
    ])

    board = cards.make_cards([
        "Q of Spades",
        "J of Spades",
        "10 of Spades",
        "2 of Hearts",
        "3 of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.STRAIGHT_FLUSH, 14)
    )


def test_straight_flush():
    hole_cards = cards.make_cards([
        "9 of Hearts",
        "8 of Hearts"
    ])

    board = cards.make_cards([
        "7 of Hearts",
        "6 of Hearts",
        "5 of Hearts",
        "2 of Clubs",
        "A of Spades"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.STRAIGHT_FLUSH, 9)
    )


def test_four_of_a_kind():
    hole_cards = cards.make_cards([
        "A of Spades",
        "A of Hearts"
    ])

    board = cards.make_cards([
        "A of Diamonds",
        "A of Clubs",
        "K of Spades",
        "2 of Hearts",
        "3 of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.FOUR_OF_A_KIND, 14, 13)
    )


def test_full_house():
    hole_cards = cards.make_cards([
        "K of Spades",
        "K of Hearts"
    ])

    board = cards.make_cards([
        "K of Diamonds",
        "7 of Clubs",
        "7 of Spades",
        "2 of Hearts",
        "3 of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.FULL_HOUSE, 13, 7)
    )


def test_flush():
    hole_cards = cards.make_cards([
        "A of Spades",
        "8 of Spades"
    ])

    board = cards.make_cards([
        "Q of Spades",
        "5 of Spades",
        "2 of Spades",
        "K of Hearts",
        "3 of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.FLUSH, 14, 12, 8, 5, 2)
    )


def test_straight():
    hole_cards = cards.make_cards([
        "A of Spades",
        "K of Hearts"
    ])

    board = cards.make_cards([
        "Q of Diamonds",
        "J of Clubs",
        "10 of Spades",
        "2 of Hearts",
        "3 of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.STRAIGHT, 14)
    )


def test_wheel():
    """
    A-2-3-4-5 straight.
    The Ace acts as the low card, so the straight is 5-high.
    """

    hole_cards = cards.make_cards([
        "A of Spades",
        "2 of Hearts"
    ])

    board = cards.make_cards([
        "3 of Diamonds",
        "4 of Clubs",
        "5 of Spades",
        "K of Hearts",
        "Q of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.STRAIGHT, 5)
    )


def test_three_of_a_kind():
    hole_cards = cards.make_cards([
        "Q of Spades",
        "Q of Hearts"
    ])

    board = cards.make_cards([
        "Q of Diamonds",
        "7 of Clubs",
        "5 of Spades",
        "2 of Hearts",
        "3 of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.THREE_OF_A_KIND, 12, 7, 5)
    )


def test_two_pair():
    hole_cards = cards.make_cards([
        "J of Spades",
        "J of Hearts"
    ])

    board = cards.make_cards([
        "7 of Diamonds",
        "7 of Clubs",
        "5 of Spades",
        "2 of Hearts",
        "3 of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.TWO_PAIR, 11, 7, 5)
    )


def test_one_pair():
    hole_cards = cards.make_cards([
        "J of Spades",
        "J of Hearts"
    ])

    board = cards.make_cards([
        "9 of Diamonds",
        "7 of Clubs",
        "5 of Spades",
        "3 of Hearts",
        "2 of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.ONE_PAIR, 11, 9, 7, 5)
    )


def test_high_card():
    hole_cards = cards.make_cards([
        "A of Spades",
        "J of Hearts"
    ])

    board = cards.make_cards([
        "9 of Diamonds",
        "7 of Clubs",
        "5 of Spades",
        "3 of Hearts",
        "2 of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.HIGH_CARD, 14, 11, 9, 7, 5)
    )

def test_wheel():
    """
    A-2-3-4-5 straight.
    Ace acts as the low card, so the straight is 5-high.
    """

    hole_cards = cards.make_cards([
        "A of Spades",
        "2 of Hearts"
    ])

    board = cards.make_cards([
        "3 of Diamonds",
        "4 of Clubs",
        "5 of Spades",
        "K of Hearts",
        "Q of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.STRAIGHT, 5)
    )


def test_wheel_straight_flush():
    """
    A-2-3-4-5 all in the same suit.
    Ace acts as the low card, so this is a 5-high straight flush.
    """

    hole_cards = cards.make_cards([
        "A of Spades",
        "2 of Spades"
    ])

    board = cards.make_cards([
        "3 of Spades",
        "4 of Spades",
        "5 of Spades",
        "K of Hearts",
        "Q of Clubs"
    ])

    check_expected_evaluation(
        hole_cards,
        board,
        (evaluator.STRAIGHT_FLUSH, 5)
    )

def test_random_hands():
    for _ in range(100000):  # Test 100000 random hands
        test_deck = deck.new_deck()
        deck.shuffle(test_deck)
        dealt_hands = deck.deal_hand(test_deck, 5)
        board = deck.deal_flop(test_deck)
        board.append(deck.deal_card(test_deck))  # Turn
        board.append(deck.deal_card(test_deck))  # River
        for hole_cards in dealt_hands:
            check_both_evaluators(hole_cards, board)
    
if __name__ == "__main__":
    """
    Run all consistency tests. 
    """
    test_royal_flush()
    test_straight_flush()
    test_four_of_a_kind()
    test_full_house()
    test_flush()
    test_straight()
    test_three_of_a_kind()
    test_two_pair()
    test_high_card()
    test_wheel()
    test_wheel_straight_flush()
    test_random_hands()
    print("\u2713 All tests passed")
