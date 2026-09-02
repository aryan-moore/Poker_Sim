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

    rank1_str = '10' if rank1 == 'T' else rank1
    rank2_str = '10' if rank2 == 'T' else rank2

    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    combos = []
    if rank1 == rank2:  # Pocket pairs
        for suit1 in range(len(suits)):
            for suit2 in range(suit1 + 1, len(suits)):
                card1 = cards.str_to_card(f"{rank1_str} of {suits[suit1]}")
                card2 = cards.str_to_card(f"{rank2_str} of {suits[suit2]}")
                combos.append((card1, card2))
    elif suited == 's': 
        for suit in range(len(suits)):
            card1 = cards.str_to_card(f"{rank1_str} of {suits[suit]}")
            card2 = cards.str_to_card(f"{rank2_str} of {suits[suit]}")
            combos.append((card1, card2))
    elif suited == 'o':
        for suit1 in range(len(suits)):
            for suit2 in range(len(suits)):
                if suit1 != suit2:
                    card1 = cards.str_to_card(f"{rank1_str} of {suits[suit1]}")
                    card2 = cards.str_to_card(f"{rank2_str} of {suits[suit2]}")
                    combos.append((card1, card2))
    else:  # Both suited and offsuit
        for suit1 in range(len(suits)):
            for suit2 in range(len(suits)):
                card1 = cards.str_to_card(f"{rank1_str} of {suits[suit1]}")
                card2 = cards.str_to_card(f"{rank2_str} of {suits[suit2]}")
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

    start_rank1, start_rank2, start_suited = parse_hand_class(start)
    end_rank1, end_rank2, end_suited = parse_hand_class(end)

    if start_suited != end_suited:
        raise ValueError(
            f"Suitedness must match in interval notation: {hand_class}"
        )

    ranks = '23456789TJQKA'

    start_index1 = ranks.index(start_rank1)
    start_index2 = ranks.index(start_rank2)
    end_index1 = ranks.index(end_rank1)
    end_index2 = ranks.index(end_rank2)

    suffix = start_suited if start_suited else ""

    expanded = []

    # Pocket pairs: 
    if (
        start_rank1 == start_rank2
        and end_rank1 == end_rank2
    ):
        if start_index1 > end_index1:
            raise ValueError(f"Invalid range order: {hand_class}")

        for i in range(start_index1, end_index1 + 1):
            expanded.append(ranks[i] + ranks[i])

    # Fixed first rank:
    elif start_rank1 == end_rank1:
        if start_index2 > end_index2:
            raise ValueError(f"Invalid range order: {hand_class}")

        for i in range(start_index2, end_index2 + 1):
            expanded.append(
                start_rank1 + ranks[i] + suffix
            )

    # Sliding interval:
    else:
        start_gap = start_index1 - start_index2
        end_gap = end_index1 - end_index2

        if start_gap != end_gap:
            raise ValueError(
                f"Invalid sliding interval: {hand_class}"
            )

        if start_index1 > end_index1:
            raise ValueError(
                f"Invalid range order: {hand_class}"
            )

        for i in range(start_index1, end_index1 + 1):
            new_rank1 = ranks[i]
            new_rank2 = ranks[i - start_gap]

            expanded.append(
                new_rank1 + new_rank2 + suffix
            )

    return expanded


def remove_blocked_combinations(combinations, known_cards):
    return [
        combo
        for combo in combinations
        if not any(card in known_cards for card in combo)
    ]


def get_legal_combinations(range_string, known_cards=None):
    hand_classes = parse_range(range_string)

    combinations = []
    seen = set()

    for hand_class in hand_classes:
        for combo in generate_combinations(hand_class):
            canonical_combo = tuple(sorted(combo))

            if canonical_combo not in seen:
                combinations.append(combo)
                seen.add(canonical_combo)

    if known_cards:
        combinations = remove_blocked_combinations(
            combinations,
            known_cards
        )

    return combinations


def count_combinations(range_string, known_cards=None):
    return len(get_legal_combinations(range_string, known_cards))


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
    try:
        parse_range(range_string)
        return True
    except ValueError:
        return False