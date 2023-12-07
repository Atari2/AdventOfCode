from __future__ import annotations
import functools
import itertools
from enum import IntEnum

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

with open(filename, "r") as f:
    lines = f.read().splitlines()

strengthsp1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
strengthsp2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

class HandType(IntEnum):
    FiveOfAKind = 1
    FourOfAKind = 2
    FullHouse = 3
    ThreeOfAKind = 4
    TwoPair = 5
    OnePair = 6
    HighCard = 7

class Hand:
    hand: str
    bet: int
    hand_type: HandType

    def __init__(self, hand: str, bet: int):
        self.hand = hand
        self.bet = bet

    def __repr__(self):
        return f"{self.hand} {self.bet} {self.hand_type.name}"

class HandPart1(Hand):

    def __init__(self, hand: str, bet: int):
        super().__init__(hand, bet)
        unique_cards = {}
        for card in hand:
            if card in unique_cards:
                unique_cards[card] += 1
            else:
                unique_cards[card] = 1
        match len(unique_cards):
            case 1:
                self.hand_type = HandType.FiveOfAKind
            case 2:
                if 4 in unique_cards.values():
                    self.hand_type = HandType.FourOfAKind
                else:
                    self.hand_type = HandType.FullHouse
            case 3:
                if 3 in unique_cards.values():
                    self.hand_type = HandType.ThreeOfAKind
                else:
                    self.hand_type = HandType.TwoPair
            case 4:
                self.hand_type = HandType.OnePair
            case 5:
                self.hand_type = HandType.HighCard

    def __lt__(self, other: HandPart1):
        if self.hand_type > other.hand_type:
            return True
        elif self.hand_type < other.hand_type:
            return False
        else:
            for sc, oc in zip(self.hand, other.hand):
                if strengthsp1.index(sc) > strengthsp1.index(oc):
                    return True
                elif strengthsp1.index(sc) < strengthsp1.index(oc):
                    return False
        
    def __gt__(self, other: HandPart1):
        return not self.__lt__(other)
    
    
    
class HandPart2(Hand):

    def _get_hand_type(self, hand: str) -> HandType:
        unique_cards = {}
        for card in hand:
            if card in unique_cards:
                unique_cards[card] += 1
            else:
                unique_cards[card] = 1
        match len(unique_cards):
            case 1:
                return HandType.FiveOfAKind
            case 2:
                if 4 in unique_cards.values():
                    return HandType.FourOfAKind
                else:
                    return HandType.FullHouse
            case 3:
                if 3 in unique_cards.values():
                    return HandType.ThreeOfAKind
                else:
                    return HandType.TwoPair
            case 4:
                return HandType.OnePair
            case 5:
                return HandType.HighCard
        raise Exception("Invalid hand")

    def __init__(self, hand: str, bet: int):
        super().__init__(hand, bet)
        j_count = hand.count('J')
        if j_count == 0:
            self.hand_type = self._get_hand_type(hand)
        else:
            self.hand_type = HandType.HighCard
            for comb in itertools.combinations_with_replacement(strengthsp2[:-1], j_count):
                hand_type = self._get_hand_type(hand.replace('J', '') + ''.join(comb))
                if self.hand_type > hand_type:
                    self.hand_type = hand_type
                if self.hand_type == HandType.FiveOfAKind:
                    break

    def __lt__(self, other: HandPart2):
        if self.hand_type > other.hand_type:
            return True
        elif self.hand_type < other.hand_type:
            return False
        else:
            for sc, oc in zip(self.hand, other.hand):
                if strengthsp2.index(sc) > strengthsp2.index(oc):
                    return True
                elif strengthsp2.index(sc) < strengthsp2.index(oc):
                    return False
        
    def __gt__(self, other: HandPart2):
        return not self.__lt__(other)

handsp1 = [HandPart1(hand, int(bet)) for hand, bet in [line.split(' ', 1) for line in lines]]
handsp1.sort()
totalp1 = functools.reduce(lambda a, ih: a + (ih[0] * ih[1].bet), enumerate(handsp1, 1), 0)

handsp2 = [HandPart2(hand, int(bet)) for hand, bet in [line.split(' ', 1) for line in lines]]
handsp2.sort()
totalp2 = functools.reduce(lambda a, ih: a + (ih[0] * ih[1].bet), enumerate(handsp2, 1), 0)
print(f'{totalp1} {totalp2}')