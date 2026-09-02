import pytest

from poker.simulation import simulator
from poker import cards


def c(card_string):
    """
    Small helper so the tests are easier to read.
    """
    return cards.str_to_card(card_string)


# ============================================================
# prepare_deck
# ============================================================

def test_prepare_deck_removes_hero_cards():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    prepared = simulator.prepare_deck(
        hero,
        [],
        []
    )

    assert hero[0] not in prepared
    assert hero[1] not in prepared

    assert len(prepared) == 50


def test_prepare_deck_removes_known_opponent_cards():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    opponents = [
        [
            c("K of Clubs"),
            c("K of Diamonds")
        ]
    ]

    prepared = simulator.prepare_deck(
        hero,
        opponents,
        []
    )

    for card in hero:
        assert card not in prepared

    for opponent in opponents:
        for card in opponent:
            assert card not in prepared

    assert len(prepared) == 48


def test_prepare_deck_removes_board_cards():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    board = [
        c("2 of Clubs"),
        c("7 of Diamonds"),
        c("J of Hearts")
    ]

    prepared = simulator.prepare_deck(
        hero,
        [],
        board
    )

    for card in hero + board:
        assert card not in prepared

    assert len(prepared) == 47


def test_prepare_deck_removes_all_known_cards():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    opponents = [
        [
            c("K of Clubs"),
            c("K of Diamonds")
        ],
        [
            c("Q of Clubs"),
            c("Q of Diamonds")
        ]
    ]

    board = [
        c("2 of Clubs"),
        c("7 of Diamonds"),
        c("J of Hearts")
    ]

    prepared = simulator.prepare_deck(
        hero,
        opponents,
        board
    )

    known_cards = (
        hero
        + opponents[0]
        + opponents[1]
        + board
    )

    for card in known_cards:
        assert card not in prepared

    # 52 - 2 hero - 4 opponent - 3 board
    assert len(prepared) == 43


# ============================================================
# deal_trial
# ============================================================

def test_deal_trial_completes_empty_board():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    prepared = simulator.prepare_deck(
        hero,
        [],
        []
    )

    random_hands, board = simulator.deal_trial(
        prepared,
        num_random_opponents=1,
        known_board=[]
    )

    assert len(random_hands) == 1
    assert len(random_hands[0]) == 2

    assert len(board) == 5


def test_deal_trial_completes_flop():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    flop = [
        c("2 of Clubs"),
        c("7 of Diamonds"),
        c("J of Hearts")
    ]

    prepared = simulator.prepare_deck(
        hero,
        [],
        flop
    )

    random_hands, board = simulator.deal_trial(
        prepared,
        num_random_opponents=1,
        known_board=flop
    )

    assert len(random_hands) == 1
    assert len(board) == 5

    # Original flop should remain at beginning of board
    assert board[:3] == flop


def test_deal_trial_completes_turn():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    turn_board = [
        c("2 of Clubs"),
        c("7 of Diamonds"),
        c("J of Hearts"),
        c("3 of Spades")
    ]

    prepared = simulator.prepare_deck(
        hero,
        [],
        turn_board
    )

    random_hands, board = simulator.deal_trial(
        prepared,
        num_random_opponents=1,
        known_board=turn_board
    )

    assert len(board) == 5
    assert board[:4] == turn_board


def test_deal_trial_full_board_does_not_add_cards():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    full_board = [
        c("2 of Clubs"),
        c("7 of Diamonds"),
        c("J of Hearts"),
        c("3 of Spades"),
        c("4 of Clubs")
    ]

    prepared = simulator.prepare_deck(
        hero,
        [],
        full_board
    )

    _, board = simulator.deal_trial(
        prepared,
        num_random_opponents=0,
        known_board=full_board
    )

    assert board == full_board


def test_deal_trial_cards_do_not_overlap():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    prepared = simulator.prepare_deck(
        hero,
        [],
        []
    )

    random_hands, board = simulator.deal_trial(
        prepared,
        num_random_opponents=3,
        known_board=[]
    )

    dealt_cards = []

    for opponent in random_hands:
        dealt_cards.extend(opponent)

    dealt_cards.extend(board)

    # Every dealt card should be unique
    assert len(dealt_cards) == len(set(dealt_cards))

    # Hero cards must not appear
    for card in hero:
        assert card not in dealt_cards


def test_deal_trial_multiple_random_opponents():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    prepared = simulator.prepare_deck(
        hero,
        [],
        []
    )

    random_hands, board = simulator.deal_trial(
        prepared,
        num_random_opponents=4,
        known_board=[]
    )

    assert len(random_hands) == 4

    for opponent in random_hands:
        assert len(opponent) == 2

    assert len(board) == 5


# ============================================================
# score_trial
# ============================================================

def test_score_trial_player_wins():

    # Hero has AA
    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    # Villain has KK
    opponent = [
        c("K of Clubs"),
        c("K of Diamonds")
    ]

    board = [
        c("2 of Clubs"),
        c("5 of Diamonds"),
        c("7 of Hearts"),
        c("9 of Spades"),
        c("J of Clubs")
    ]

    result = simulator.score_trial(
        hero,
        [opponent],
        board
    )

    assert result == 0


def test_score_trial_player_loses():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    opponent = [
        c("K of Clubs"),
        c("K of Diamonds")
    ]

    # King on board gives villain three kings.
    board = [
        c("K of Hearts"),
        c("5 of Diamonds"),
        c("7 of Hearts"),
        c("9 of Spades"),
        c("J of Clubs")
    ]

    result = simulator.score_trial(
        hero,
        [opponent],
        board
    )

    assert result == 2


def test_score_trial_tie():

    hero = [
        c("2 of Clubs"),
        c("3 of Clubs")
    ]

    opponent = [
        c("4 of Diamonds"),
        c("5 of Diamonds")
    ]

    # Royal flush entirely on board.
    # Everyone plays the board.
    board = [
        c("10 of Spades"),
        c("J of Spades"),
        c("Q of Spades"),
        c("K of Spades"),
        c("A of Spades")
    ]

    result = simulator.score_trial(
        hero,
        [opponent],
        board
    )

    assert result == 1


def test_score_trial_losing_to_one_opponent_means_loss():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    weaker_opponent = [
        c("Q of Clubs"),
        c("Q of Diamonds")
    ]

    stronger_opponent = [
        c("K of Clubs"),
        c("K of Diamonds")
    ]

    board = [
        c("K of Hearts"),
        c("5 of Diamonds"),
        c("7 of Hearts"),
        c("9 of Spades"),
        c("J of Clubs")
    ]

    result = simulator.score_trial(
        hero,
        [
            weaker_opponent,
            stronger_opponent
        ],
        board
    )

    assert result == 2


def test_score_trial_loss_overrides_tie():

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    tying_opponent = [
        c("A of Clubs"),
        c("A of Diamonds")
    ]

    winning_opponent = [
        c("K of Clubs"),
        c("K of Diamonds")
    ]

    board = [
        c("K of Hearts"),
        c("5 of Diamonds"),
        c("7 of Hearts"),
        c("9 of Spades"),
        c("J of Clubs")
    ]

    result = simulator.score_trial(
        hero,
        [
            tying_opponent,
            winning_opponent
        ],
        board
    )

    assert result == 2


# ============================================================
# simulate_equity
# ============================================================

def test_simulate_equity_counts_all_trials(monkeypatch):

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    # Force Monte Carlo rather than exact enumeration.
    monkeypatch.setattr(
        simulator.exact_solver,
        "should_use_exact",
        lambda *args: False
    )

    wins, ties, losses = simulator.simulate_equity(
        hero,
        num_random_opponents=1,
        num_trials=100
    )

    assert wins + ties + losses == 100


def test_simulate_equity_known_opponent_counts_trials(monkeypatch):

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    opponent = [
        [
            c("K of Clubs"),
            c("K of Diamonds")
        ]
    ]

    monkeypatch.setattr(
        simulator.exact_solver,
        "should_use_exact",
        lambda *args: False
    )

    wins, ties, losses = simulator.simulate_equity(
        hero,
        known_opponent_hands=opponent,
        num_trials=100
    )

    assert wins + ties + losses == 100


def test_simulate_equity_mix_known_and_random_opponents(monkeypatch):

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    known_opponent = [
        [
            c("K of Clubs"),
            c("K of Diamonds")
        ]
    ]

    monkeypatch.setattr(
        simulator.exact_solver,
        "should_use_exact",
        lambda *args: False
    )

    wins, ties, losses = simulator.simulate_equity(
        hero,
        known_opponent_hands=known_opponent,
        num_random_opponents=1,
        num_trials=100
    )

    assert wins + ties + losses == 100


def test_simulate_equity_with_known_board(monkeypatch):

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    opponent = [
        [
            c("K of Clubs"),
            c("K of Diamonds")
        ]
    ]

    flop = [
        c("2 of Clubs"),
        c("5 of Diamonds"),
        c("7 of Hearts")
    ]

    monkeypatch.setattr(
        simulator.exact_solver,
        "should_use_exact",
        lambda *args: False
    )

    wins, ties, losses = simulator.simulate_equity(
        hero,
        known_opponent_hands=opponent,
        known_board=flop,
        num_trials=100
    )

    assert wins + ties + losses == 100


# ============================================================
# Exact-solver branch
# ============================================================

def test_simulate_equity_uses_exact_solver(monkeypatch):

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    expected_result = (100, 5, 10)

    monkeypatch.setattr(
        simulator.exact_solver,
        "should_use_exact",
        lambda *args: True
    )

    monkeypatch.setattr(
        simulator.exact_solver,
        "enumerate_exact",
        lambda *args: expected_result
    )

    result = simulator.simulate_equity(
        hero,
        num_random_opponents=1
    )

    assert result == expected_result


def test_simulate_equity_does_not_use_exact_solver_when_not_needed(
    monkeypatch
):

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    monkeypatch.setattr(
        simulator.exact_solver,
        "should_use_exact",
        lambda *args: False
    )

    exact_called = False

    def fake_exact(*args):
        nonlocal exact_called
        exact_called = True
        return (0, 0, 0)

    monkeypatch.setattr(
        simulator.exact_solver,
        "enumerate_exact",
        fake_exact
    )

    simulator.simulate_equity(
        hero,
        num_random_opponents=1,
        num_trials=10
    )

    assert not exact_called


# ============================================================
# Deterministic simulate_equity aggregation tests
# ============================================================

def test_simulate_equity_records_wins_correctly(monkeypatch):

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    monkeypatch.setattr(
        simulator.exact_solver,
        "should_use_exact",
        lambda *args: False
    )

    # We don't care about actual dealing for this unit test.
    monkeypatch.setattr(
        simulator,
        "deal_trial",
        lambda *args: ([], [])
    )

    monkeypatch.setattr(
        simulator,
        "score_trial",
        lambda *args: 0
    )

    wins, ties, losses = simulator.simulate_equity(
        hero,
        num_trials=20
    )

    assert wins == 20
    assert ties == 0
    assert losses == 0


def test_simulate_equity_records_ties_correctly(monkeypatch):

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    monkeypatch.setattr(
        simulator.exact_solver,
        "should_use_exact",
        lambda *args: False
    )

    monkeypatch.setattr(
        simulator,
        "deal_trial",
        lambda *args: ([], [])
    )

    monkeypatch.setattr(
        simulator,
        "score_trial",
        lambda *args: 1
    )

    wins, ties, losses = simulator.simulate_equity(
        hero,
        num_trials=20
    )

    assert wins == 0
    assert ties == 20
    assert losses == 0


def test_simulate_equity_records_losses_correctly(monkeypatch):

    hero = [
        c("A of Spades"),
        c("A of Hearts")
    ]

    monkeypatch.setattr(
        simulator.exact_solver,
        "should_use_exact",
        lambda *args: False
    )

    monkeypatch.setattr(
        simulator,
        "deal_trial",
        lambda *args: ([], [])
    )

    monkeypatch.setattr(
        simulator,
        "score_trial",
        lambda *args: 2
    )

    wins, ties, losses = simulator.simulate_equity(
        hero,
        num_trials=20
    )

    assert wins == 0
    assert ties == 0
    assert losses == 20