from poker import cards

def parse_hand_class(hand_class: str) -> tuple[str, str, str | None]:
    rank1 = hand_class[0]
    rank2 = hand_class[1]
    suited = None
    if len(hand_class) == 3:
        suited = hand_class[2]
    return (rank1, rank2, suited)

def generate_combinations(hand_class):
    if not validate_hand_class(hand_class):
        raise ValueError(f"Invalid hand class: {hand_class}")
    rank1, rank2, suited = parse_hand_class(hand_class)
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    combos = []
    if rank1 == rank2:  # Pocket pairs
        for suit1 in range(len(suits)):
            for suit2 in range(suit1 + 1, len(suits)):
                card1 = cards.str_to_card(f"{rank1} of {suits[suit1]}")
                card2 = cards.str_to_card(f"{rank2} of {suits[suit2]}")
                combos.append((card1, card2))
    elif suited == 's': 
        for suit in range(len(suits)):
            card1 = cards.str_to_card(f"{rank1} of {suits[suit]}")
            card2 = cards.str_to_card(f"{rank2} of {suits[suit]}")
            combos.append((card1, card2))
    elif suited == 'o':
        for suit1 in range(len(suits)):
            for suit2 in range(len(suits)):
                if suit1 != suit2:
                    card1 = cards.str_to_card(f"{rank1} of {suits[suit1]}")
                    card2 = cards.str_to_card(f"{rank2} of {suits[suit2]}")
                    combos.append((card1, card2))
    else:  # Both suited and offsuit
        for suit1 in range(len(suits)):
            for suit2 in range(len(suits)):
                card1 = cards.str_to_card(f"{rank1} of {suits[suit1]}")
                card2 = cards.str_to_card(f"{rank2} of {suits[suit2]}")
                combos.append((card1, card2))
    return combos


def parse_range(range_string):
    hand_classes = [
        hand_class.strip()
        for hand_class in range_string.split(',')
    ]

    expanded = []
    seen = set()

    for hand_class in hand_classes:
        if hand_class.endswith('+'):
            new_hands = expand_plus_notation(hand_class)
        elif '-' in hand_class:
            new_hands = expand_interval_notation(hand_class)
        else:
            if not validate_hand_class(hand_class):
                raise ValueError(f"Invalid hand class: {hand_class}")
            new_hands = [hand_class]

        for new_hand in new_hands:
            if new_hand not in seen:
                expanded.append(new_hand)
                seen.add(new_hand)

    return expanded


def expand_plus_notation(hand_class):
    if not hand_class.endswith('+'):
        return [hand_class]

    base_hand = hand_class[:-1]

    if not validate_hand_class(base_hand):
        raise ValueError(f"Invalid hand class: {base_hand}")

    ranks = '23456789TJQKA'
    rank1, rank2, suited = parse_hand_class(base_hand)
    expanded = []

    if rank1 == rank2:  # Pocket pairs
        start_index = ranks.index(rank1)
        for i in range(start_index, len(ranks)):
            expanded.append(ranks[i] + ranks[i])
    else:  # Non-pair hands
        start_index1 = ranks.index(rank1)
        start_index2 = ranks.index(rank2)

        for i in range(start_index2, start_index1):
            new_hand = rank1 + ranks[i]
            if suited:
                new_hand += suited
            expanded.append(new_hand)
    return expanded

def expand_interval_notation(hand_class):
    if '-' not in hand_class:
        return [hand_class]

    start, end = hand_class.split('-')

    if not validate_hand_class(start) or not validate_hand_class(end):
        raise ValueError(f"Invalid range: {hand_class}")

    start_rank1, start_rank2, _ = parse_hand_class(start)
    end_rank1, end_rank2, _ = parse_hand_class(end)

    if (
        start_rank1 != start_rank2
        or end_rank1 != end_rank2
    ):
        raise ValueError(
            f"Only pocket-pair intervals are currently supported: {hand_class}"
        )

    ranks = '23456789TJQKA'
    start_index = ranks.index(start_rank1)
    end_index = ranks.index(end_rank1)

    if start_index > end_index:
        raise ValueError(f"Invalid range order: {hand_class}")

    expanded = []
    for i in range(start_index, end_index + 1):
        expanded.append(ranks[i] + ranks[i])
    return expanded


def remove_blocked_combinations(combinations, known_cards):
    for combo in combinations:
        if any(card in known_cards for card in combo):
            combinations.remove(combo)
    return combinations


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
    if('23456789TJQKA'.index(hand_class[0]) < '23456789TJQKA'.index(hand_class[1])):
        return False
    return True


def validate_range(range_string):
    pass