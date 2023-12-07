from enum import IntEnum
from collections import Counter

INPUT = "input.txt"
# INPUT = "07.ex"

face_cards = {
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

def parse_input(file=INPUT):
    # Returns list of tuples (hand, bid)
    with open(file) as f:
        return [tuple(line.split()) for line in f.readlines()]

def card_to_value(card_str, p1=True):
    try:
        return int(card_str)
    except ValueError:
        return face_cards[card_str]

class HandType(IntEnum):
    FIVE_KIND = 6
    FOUR_KIND = 5
    FULL_HOUSE = 4
    THREE_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0

class Hand:
    def __init__(self, hand_str, bid):
        self.hand = hand_str
        self.bid = int(bid)
        self.cards = [card_to_value(c) for c in hand_str]

    @property
    def hand_type(self):
        card_set = set(self.cards)

        match len(card_set):
            case 1:
                return HandType.FIVE_KIND

            case 2:
                if self.hand.count(self.hand[0]) in [2, 3]:
                    return HandType.FULL_HOUSE

                return HandType.FOUR_KIND

            case 3:
                for card in card_set:
                    if self.cards.count(card) == 3:
                        return HandType.THREE_KIND

                return HandType.TWO_PAIR

            case 4:
                return HandType.ONE_PAIR

            case _:
                return HandType.HIGH_CARD

    @property
    def best_hand(self):
        num_jokers = self.hand.count('J')

        if num_jokers == 0:
            best_hand = self.hand
        elif num_jokers == 5:
            best_hand = 'AAAAA'
        else:
            # Always want to make Joker the most frequent card
            non_joker_hand = ''.join([c for c in self.hand if c != 'J'])
            non_joker_card_counts = Counter(non_joker_hand) 
            most_freq_card = non_joker_card_counts.most_common()[0][0]
            best_hand = non_joker_hand + (num_jokers * most_freq_card)

        return Hand(best_hand, self.bid)

    @property
    def cards_p2(self):
        return [
            card if card != card_to_value('J') else 0
            for card in self.cards
        ]


if __name__ == "__main__":
    hand_list = parse_input()
    hands = [Hand(h[0], h[1]) for h in hand_list]

    p1_hands = sorted(hands, key=lambda h: (h.hand_type, h.cards))
    p1_score = sum([
        (rank + 1) * hand.bid
        for rank, hand in enumerate(p1_hands)
    ])
    print(p1_score)

    p2_hands = sorted(hands, key=lambda h: (h.best_hand.hand_type, h.cards_p2))
    p2_score = sum([
        (rank + 1) * hand.bid
        for rank, hand in enumerate(p2_hands)
    ])
    print(p2_score)

