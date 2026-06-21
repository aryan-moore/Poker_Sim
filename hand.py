def make_hand(hole_cards, community_cards):
    hand = list(hole_cards) + list(community_cards)
    hand.sort()
    return hand

def hand_contains(hand, card):
    return card in hand

