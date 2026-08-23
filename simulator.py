import deck
import hand
import cards
import evaluator
import fast_evaluator
import exact_solver

def prepare_deck(hole_cards, known_opponent_hands, known_board):
    """
    Build a fresh deck with every known card removed: the player's hole
    cards, every known opponent's hole cards, and any known board cards.
    """
    deck_list = deck.new_deck()
    for card in hole_cards:
        deck.remove_card(deck_list, card)
    for opp_hand in known_opponent_hands:
        for card in opp_hand:
            deck.remove_card(deck_list, card)
    for card in known_board:
        deck.remove_card(deck_list, card)
    return deck_list


def deal_trial(prepared_deck, num_random_opponents, known_board):
    """
    Deal one random trial: hole cards for any remaining unknown opponents,
    plus however many board cards are still unknown.
    Returns (random_opponent_hands, full_board).
    """
    pd = prepared_deck.copy()
    deck.shuffle(pd)

    random_opponent_hands = deck.deal_hand(pd, num_random_opponents)

    cards_needed = 5 - len(known_board)
    dealt = []
    # loop: deal that many individual cards with deck.deal_card()
    for _ in range(cards_needed):
        dealt.append(deck.deal_card(pd))
    full_board = known_board + dealt
    return random_opponent_hands, full_board

def score_trial(hole_cards, opponent_hands, board):
    """
    Score a single trial: returns whether hole_cards win, lose, or tie 
    against the given opponent_hands and board.
    """
    player_score = fast_evaluator.evaluate_hand(hand.make_hand(hole_cards,board))
    wlt = 0 # 0 = win, 1 = tie, 2 = lose
    for opp_hand in opponent_hands:
        opp_score = fast_evaluator.evaluate_hand(hand.make_hand(opp_hand,board))
        if player_score < opp_score:
            wlt = 2
        if player_score == opp_score and wlt != 2:
            wlt = 1
    return wlt

def simulate_equity(hole_cards, known_opponent_hands=None, num_random_opponents=0,
                     known_board=None, num_trials=20000):
    """
    Unified equity simulator. Handles any mix of:
      - fully random opponents (num_random_opponents > 0)
      - fully known opponents (known_opponent_hands)
      - both at once
      - any known board state -- empty (preflop), partial (flop/turn), or full (river)
    Returns (wins, ties, losses).
    """
    known_opponent_hands = known_opponent_hands if known_opponent_hands is not None else []
    known_board = known_board if known_board is not None else []

    prepared_deck = prepare_deck(hole_cards, known_opponent_hands, known_board)

    wins = ties = losses = 0

    if exact_solver.should_use_exact(num_random_opponents, 5 - len(known_board), len(prepared_deck)):
        return exact_solver.enumerate_exact(hole_cards, known_opponent_hands, num_random_opponents, prepared_deck, known_board)

    for _ in range(num_trials):
        random_hands, board = deal_trial(prepared_deck, num_random_opponents, known_board)
        opponent_hands = known_opponent_hands + random_hands
        result = score_trial(hole_cards, opponent_hands, board)
        if result == 0:
            wins += 1
        elif result == 1:
            ties += 1
        else:
            losses += 1

    return wins, ties, losses

if __name__ == "__main__":
    # Example usage: simulate equity of AA against a random opponent over 100,000 trials
    hole_cards = [cards.str_to_card("A of Spades"), cards.str_to_card("A of Hearts")]  # Example: Ace of Spades and Ace of Hearts
    num_opponents = 1
    num_trials = 100000
    wins, ties, losses = simulate_equity(hole_cards, num_random_opponents=num_opponents, num_trials=num_trials)
    print(f"Wins: {wins}, Ties: {ties}, Losses: {losses}")
    # Example usage: simulate equity of AA against a known opponent hand over 100,000 trials
    opponent_hands = [[cards.str_to_card("K of Clubs"), cards.str_to_card("K of Diamonds")]]  # Example: King of Spades and King of Hearts
    wins, ties, losses = simulate_equity(hole_cards, known_opponent_hands=opponent_hands, num_trials=num_trials)
    print(f"Wins: {wins}, Ties: {ties}, Losses: {losses}")
    # Example usage: simulate equity of AA against known opponent hands over 100,000 trials
    opponent_hands = [
        [cards.str_to_card("K of Clubs"), cards.str_to_card("K of Hearts")],  # Example: King of Clubs and King of Diamonds
        [cards.str_to_card("10 of Diamonds"), cards.str_to_card("J of Diamonds")]   # Example: 10 of Diamonds and Jack of Diamonds
    ]
    wins, ties, losses = simulate_equity(hole_cards, known_opponent_hands=opponent_hands, num_trials=num_trials)
    print(f"Wins: {wins}, Ties: {ties}, Losses: {losses}")