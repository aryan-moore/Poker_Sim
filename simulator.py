import deck
import hand
import cards
import evaluator
import fast_evaluator

def prepare_deck(hole_cards):
    """
    Build a fresh 52-card deck with the given hole cards removed,
    so it's ready to deal opponents' cards and the board from.
    """
    deck_list = deck.new_deck()
    for card in hole_cards:
        deck.remove_card(deck_list, card)
    return deck_list

def prepare_deck_known(hole_cards, opponent_hands):
    """
    Build a fresh 52-card deck with the player's hole cards AND every
    known opponent's hole cards removed, ready to deal a random board from.
    """
    deck_list = deck.new_deck()
    for card in hole_cards:
        deck.remove_card(deck_list, card)
    for opp_hand in opponent_hands:
        for card in opp_hand:
            deck.remove_card(deck_list, card)
    return deck_list

def deal_trial_known(prepared_deck, opponent_hands):
    """
    Deal one random trial from the prepared deck: a 5-card board.
    Returns (opponent_hands, board).
    """
    pd = prepared_deck.copy()  # Make a copy of the prepared deck to shuffle and deal from
    deck.shuffle(pd)
    board = deck.deal_flop(pd)
    board.append(deck.deal_card(pd))  # Turn
    board.append(deck.deal_card(pd))  # River
    return (opponent_hands, board)

def simulate_equity_known(hole_cards, opponent_hands, num_trials):
    """
    Simulate a number of trials to estimate the equity of hole_cards
    against the given opponent_hands. Returns (wins, ties, losses).
    """
    prepared_deck = prepare_deck_known(hole_cards, opponent_hands)
    wins = 0
    ties = 0
    losses = 0
    for _ in range(num_trials):
        opponent_hands, board = deal_trial_known(prepared_deck, opponent_hands)
        result = score_trial(hole_cards, opponent_hands, board)
        if result == 0:
            wins += 1
        elif result == 1:
            ties += 1
        else:
            losses += 1
    return (wins, ties, losses)

def deal_trial(prepared_deck, num_opponents):
    """
    Deal one random trial from the prepared deck: hole cards for each
    opponent, plus a 5-card board. Returns (opponent_hands, board).
    """
    pd = prepared_deck.copy()  # Make a copy of the prepared deck to shuffle and deal from
    deck.shuffle(pd)
    opponent_hands = deck.deal_hand(pd, num_opponents)
    board = deck.deal_flop(pd)
    board.append(deck.deal_card(pd))  # Turn
    board.append(deck.deal_card(pd))  # River
    return (opponent_hands, board)

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

def simulate_equity(hole_cards, num_opponents, num_trials):
    """
    Simulate a number of trials to estimate the equity of hole_cards
    against num_opponents random hands. Returns (wins, ties, losses).
    """
    prepared_deck = prepare_deck(hole_cards)
    wins = 0
    ties = 0
    losses = 0
    for _ in range(num_trials):
        opponent_hands, board = deal_trial(prepared_deck, num_opponents)
        result = score_trial(hole_cards, opponent_hands, board)
        if result == 0:
            wins += 1
        elif result == 1:
            ties += 1
        else:
            losses += 1
    return (wins, ties, losses)

if __name__ == "__main__":
    # Example usage: simulate equity of AA against a random opponent over 100,000 trials
    hole_cards = [cards.str_to_card("A of Spades"), cards.str_to_card("A of Hearts")]  # Example: Ace of Spades and Ace of Hearts
    num_opponents = 1
    num_trials = 100000
    wins, ties, losses = simulate_equity(hole_cards, num_opponents, num_trials)
    print(f"Wins: {wins}, Ties: {ties}, Losses: {losses}")