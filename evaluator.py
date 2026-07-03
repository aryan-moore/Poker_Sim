import deck
import cards
import hand

def evaluate_hand(hand):
    # Placeholder for hand evaluation logic
    # This function should return hand representation
    if (isStraightFlush(hand)):
        return 
    return 0

def isStraightFlush(hand):
    for i in range(len(hand) - 4, -1, -1):
        if (hand[i] + 3 == hand[i+3] and hand[i] // 13 == hand[i+3] // 13 and hand[i]%13 == 9 and  hand[i+3] - 12 in hand):
             return [10, 0]  # Royal Flush, return rank of Ace
        if (i + 4 < len(hand) and hand[i] + 4 == hand[i+4] and hand[i] // 13 == hand[i+4] // 13):
            return [9, hand[i+4]%13]  # Straight Flush, return rank of highest card
    return False

def isFourOfAKind(hand):
    ranks = [card % 13 for card in hand]

    counts = [0] * 13

    for card in hand:
        counts[card % 13] += 1

    for rank in range(12, -1, -1):
        if counts[rank] == 4:
            for kicker_rank in range(12, -1, -1):
                if kicker_rank != rank and counts[kicker_rank] > 0:
                    return [8, rank, kicker_rank]  # Four of a Kind, return rank of four cards and kicker
    return False

def isFullHouse(hand):
    # Placeholder for checking if the hand is a Full House
    return False

def isFlush(hand):
    suit_counts = [0, 0, 0, 0]
    final = []
    for card in hand:
        suit_counts[card // 13] += 1
    if any(count >= 5 for count in suit_counts):
        final.append(6)  # Flush, return rank of highest card
    else:
        return False
    for card in reversed(hand):
        if suit_counts[card // 13] >= 5:
            final.append(card % 13)
        if len(final) == 6:
            break
    return final   

def isStraight(hand):
    ranks = [card % 13 for card in hand]
    ranks = list(set(ranks))  # Remove duplicates
    ranks.sort()
    if len(ranks) < 5: return False  # Not enough unique ranks for a straight
    for i in range(len(ranks) - 4, -1, -1):
        if (ranks[i] + 3 == ranks[i+3] and ranks[i] == 9 and 0 in ranks):
             return [5, 0]  # Broadway Straight, return rank of Ace
        if (i + 4 < len(ranks) and ranks[i] + 4 == ranks[i+4]):
            return [5, ranks[i+4]]  # Straight, return rank of highest card
    return False

def isThreeOfAKind(hand):        
    # Placeholder for checking if the hand is Three of a Kind
    return False    

def isTwoPair(hand):
    # Placeholder for checking if the hand is Two Pair
    return False

def isOnePair(hand):
    # Placeholder for checking if the hand is One Pair
    return False

def isHighCard(hand):
    # Placeholder for checking if the hand is a High Card
    return False