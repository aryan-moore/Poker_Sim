import math
import cards
import fast_evaluator
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