import deck
import cards

def evaluate_hand(hand):
    # Placeholder for hand evaluation logic
    # This function should return hand represnentation
    if (isStraightFlush(hand)):
        return 
    return 0

def isStraightFlush(hand):
    for i in range(len(hand) - 4, -1, -1):
        if (hand[i] + 4 == hand[i+4] and hand[i] // 13 == hand[i+4] // 13):
            return [9, hand[i+4]%13]  # Straight Flush, return rank of highest card
    return False

def isFourOfAKind(hand):
    # Placeholder for checking if the hand is Four of a Kind
    return False

def isFullHouse(hand):
    # Placeholder for checking if the hand is a Full House
    return False

def isFlush(hand):
    # Placeholder for checking if the hand is a Flush
    return False    

def isStraight(hand):
    # Placeholder for checking if the hand is a Straight
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