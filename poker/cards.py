# Return the rank of the card
# 2 = 0, 3 = 1, ..., K = 11, A = 12
def rank_card(card):
    return card % 13

def str_to_rank(rank_str):
    ranks = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
    return ranks[rank_str]
 
# Return the suit of the card
# Spades = 0, Hearts = 1, Diamonds = 2, Clubs = 3
def suit_card(card):
    return card // 13

def str_to_suit(suit_str):
    suits = {'Spades': 0, 'Hearts': 1, 'Diamonds': 2, 'Clubs': 3}
    return suits[suit_str]
 
# Return a string representation of the card
def card_str(card):
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    rank = ranks[rank_card(card)]
    suit = suits[suit_card(card)]
    return f"{rank} of {suit}"

def str_to_card(card_str):
    ranks = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
    suits = {'Spades': 0, 'Hearts': 1, 'Diamonds': 2, 'Clubs': 3}
    rank_str, suit_str = card_str.split(' of ')
    rank = ranks[rank_str]
    suit = suits[suit_str]
    return suit * 13 + rank

def make_cards(card_strings):
    return [str_to_card(card_str) for card_str in card_strings]