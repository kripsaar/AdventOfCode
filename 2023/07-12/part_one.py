from functools import total_ordering
from enum import IntEnum
from bisect import insort

class HandType(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

card_types = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def determine_hand_type(hand_str: str) -> HandType:
    unique_chars = set(hand_str)
    if len(unique_chars) == 1:
        return HandType.FIVE_OF_A_KIND
    if len(unique_chars) == 4:
        return HandType.ONE_PAIR
    if len(unique_chars) == 3:
        for char in unique_chars:
            if hand_str.count(char) == 3:
                return HandType.THREE_OF_A_KIND
        return HandType.TWO_PAIR
    if len(unique_chars) == 2:
        for char in unique_chars:
            if hand_str.count(char) == 4:
                return HandType.FOUR_OF_A_KIND
        return HandType.FULL_HOUSE
    return HandType.HIGH_CARD

@total_ordering
class Hand:
    def __init__(self, hand_str: str) -> None:
        self.hand_str = hand_str
        self.hand_type = determine_hand_type(hand_str)

    def __repr__(self) -> str:
        return self.hand_str
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        self.hand_str == other.hand_str

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        if not self.hand_type == other.hand_type:
            return self.hand_type > other.hand_type
        for idx in range(5):
            l = card_types[self.hand_str[idx]]
            r = card_types[other.hand_str[idx]]
            if not l == r:
                return l > r
        return False
    
def parse_input(filename):
    bids = {}
    hands: list[Hand] = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            hand_str, bid_str = line.split()
            bid = int(bid_str)
            bids[hand_str] = bid
            hand = Hand(hand_str)
            insort(hands, hand)
    return bids, hands

bids, hands = parse_input('input-07')
result = 0
for idx, hand in enumerate(hands):
    result += (idx + 1) * bids[hand.hand_str]

print(result)