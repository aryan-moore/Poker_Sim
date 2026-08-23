import math
import cards
import fast_evaluator
import itertools
import simulator
import deck

def search_space_size(num_random_opponents, cards_needed_board, deck_size):
    """
    How many distinct exact scenarios there are to check, given how many
    cards are still unknown. Returns None if exact enumeration isn't
    supported for this shape of problem (2+ random opponents).
    """
    if num_random_opponents == 0:
        return math.comb(deck_size, cards_needed_board)

    if num_random_opponents == 1:
        return math.comb(deck_size, 2) * math.comb(deck_size - 2, cards_needed_board)

    return None  # 2+ random opponents: not supported yet, always use Monte Carlo

MAX_EXACT_SEARCH_SPACE = 2_000_000

def should_use_exact(num_random_opponents, cards_needed_board, deck_size):
    """
    Decide whether exact enumeration is feasible for this scenario.
    Returns True if it is, False if Monte Carlo should be used instead.
    """
    size = search_space_size(num_random_opponents, cards_needed_board, deck_size)

    if size is None:
        return False

    return size < MAX_EXACT_SEARCH_SPACE

def enumerate_exact(hole_cards, known_opponent_hands, num_random_opponents, prepared_deck, known_board):
    """
    Exhaustively enumerate every possible outcome (no random opponents,
    or exactly 1) and tally wins/ties/losses exactly -- zero statistical
    noise, unlike simulate_equity's sampling approach.
    Returns (wins, ties, losses).
    """
    cards_needed_board = 5 - len(known_board)
    wins = ties = losses = 0
    if num_random_opponents == 0:
        # Only the board is unknown -- iterate every possible board directly
        for board_combo in itertools.combinations(prepared_deck, cards_needed_board):
            board = known_board + list(board_combo)
            simulator_score = simulator.score_trial(hole_cards, known_opponent_hands, board)
            if simulator_score == 2:
                losses += 1
            elif simulator_score == 1:
                ties +=1
            else:
                wins +=1
                

    elif num_random_opponents == 1:
        # Iterate every possible opponent hand, and for each one, every
        # possible remaining board
        for opp_hand_combo in itertools.combinations(prepared_deck, 2):
            remaining_after_opp = [c for c in prepared_deck if c not in opp_hand_combo]
            for board_combo in itertools.combinations(remaining_after_opp, cards_needed_board):
                board = known_board + list(board_combo)
                opponent_hands = known_opponent_hands + [list(opp_hand_combo)]
                # your code here -- same idea, score and tally

    return wins, ties, losses