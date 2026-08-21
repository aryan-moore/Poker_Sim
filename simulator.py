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