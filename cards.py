# Return the rank of the card
# 2 = 0, 3 = 1, ..., K = 11, A = 12
def rank_card(card):
    return card % 13
 
# Return the suit of the card
# Spades = 0, Hearts = 1, Diamonds = 2, Clubs = 3
def suit_card(card):
    return card // 13
 
# Return a string representation of the card
def card_str(card):
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    rank = ranks[rank_card(card)]
    suit = suits[suit_card(card)]
    return f"{rank} of {suit}"