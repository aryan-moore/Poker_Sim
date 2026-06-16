def make_hand(hole_cards, community_cards):
    hand = list(hole_cards) + list(community_cards)
    hand.sort()
    return hand


