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


class Hand:
    def __init__(self, hand_str, bid):
        self.hand = hand_str
        self.bid = int(bid)
        self.cards = [face_cards.get(c) or int(c) for c in hand_str]

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


if __name__ == "__main__":
    hands = [Hand(h[0], h[1]) for h in parse_input()]

    p1_hands = sorted(
        hands,
        key=lambda h: (
            # Shorter set = fewer card values in hand
            -len(set(h.cards)),
            # Higher max card freq = better hand
            Counter(h.cards).most_common(1)[0][1],
            # Tiebreak: values of actual cards
            h.cards
        )
    )

    p1_score = sum([
        (rank + 1) * hand.bid
        for rank, hand in enumerate(p1_hands)
    ])
    print(p1_score)

    # Sort by best hand instead of actual hand for p2
    p2_hands = sorted(
        hands,
        key=lambda h: (
            -len(set(h.best_hand.cards)),
            Counter(h.best_hand.cards).most_common(1)[0][1],
            # J = 0 for part 2
            [c if c != face_cards['J'] else 0 for c in h.cards]
        )
    )

    p2_score = sum([
        (rank + 1) * hand.bid
        for rank, hand in enumerate(p2_hands)
    ])
    print(p2_score)
