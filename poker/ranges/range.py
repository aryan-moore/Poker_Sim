from poker import cards

def parse_hand_class(hand_class: str) -> set:
    rank1 = hand_class[0]
    rank2 = hand_class[1]
    suited = None
    if len(hand_class) == 3:
        suited = hand_class[2]
    return (rank1, rank2, suited)

def generate_combinations(hand_class):
    if not validate_hand_class(hand_class):
        raise ValueError(f"Invalid hand class: {hand_class}")
    hand_class = parse_hand_class(hand_class)
    combos = []
    if hand_class[2] == 's': 
        for suit in ['Spades', 'Hearts', 'Diamonds', 'Clubs']:
            card1 = cards.str_to_card(f"{hand_class[0]} of {suit}")
            card2 = cards.str_to_card(f"{hand_class[1]} of {suit}")
            combos.append((card1, card2))
    else:
        for suit1 in ['Spades', 'Hearts', 'Diamonds', 'Clubs']:
            for suit2 in ['Spades', 'Hearts', 'Diamonds', 'Clubs']:
                if suit1 != suit2:
                    card1 = cards.str_to_card(f"{hand_class[0]} of {suit1}")
                    card2 = cards.str_to_card(f"{hand_class[1]} of {suit2}")
                    combos.append((card1, card2))
    return combos


def parse_range(range_string):
    pass


def expand_plus_notation(hand_class):
    pass


def remove_blocked_combinations(combinations, known_cards):
    
    pass


def get_legal_combinations(range_string, known_cards=None):
    pass


def count_combinations(range_string, known_cards=None):
    pass


def validate_hand_class(hand_class):
    if(len(hand_class) < 2 or len(hand_class) > 3):
        return False
    if(hand_class[0] not in '23456789TJQKA' or hand_class[1] not in '23456789TJQKA'):
        return False
    if(len(hand_class) == 3 and (hand_class[2] != 's' and hand_class[2] != 'o')):
        return False
    if(hand_class[0] == hand_class[1] and len(hand_class) == 3):
        return False
    return True


def validate_range(range_string):
    pass