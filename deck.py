import random

# A deck of cards is represented as a list of integers from 0 to 51, 
# where each integer corresponds to a specific card.
def new_deck():
    return list(range(52))

# Shuffle the deck of cards in place
def shuffle(deck):
    random.shuffle(deck)

def deal_hand(deck, num_players):
    # Deal 2 cards to each player
    dealt = deck[:num_players * 2]
    del deck[:num_players * 2]  # Remove the dealt cards from the deck
    hands = []
    for i in range(num_players):
        hand = [dealt[i], dealt[i + num_players]]
        hands.append(hand)
    return hands

def deal_flop(deck):
    # Deal 3 community cards
    flop = deck[:3]
    del deck[:3]  # Remove the dealt cards from the deck
    return flop

def deal_card(deck):
    # Deal 1 community card
    turn = deck[0]
    deck.pop(0)  # Remove the dealt card from the deck
    return turn

def burn_card(deck):
    # Remove the top card from the deck
    deck.pop(0)

def find_card(deck, card):
    # Return the index of the card in the deck, or -1 if not found
    try:
        return deck.index(card)
    except ValueError:
        return -1
    
def remove_card(deck, card):
    # Remove the specified card from the deck
    index = find_card(deck, card)
    if index != -1:
        del deck[index]