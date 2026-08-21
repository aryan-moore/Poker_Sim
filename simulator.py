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