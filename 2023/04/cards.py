
def parse_card(card):
    _, nums = card.split(':')
    nums = nums.strip()
    winning_tokens, mine_tokens = [t.strip() for t in nums.split('|')]
    winning = [int(t) for t in winning_tokens.split()]
    mine = [int(t) for t in mine_tokens.split()]
    return winning, mine

if __name__ == "__main__":
    lines = []
    with open('input.txt') as f:
        lines = f.readlines()

    copies = [1 for _ in lines]
    total_points = 0

    for card_num, card in enumerate(lines):
        winning, mine = parse_card(card.strip())

        winning_nums = 0
        points = 0

        for num in winning:
            if num in mine:
                winning_nums += 1

                if winning_nums == 1:
                    points += 1
                else:
                    points *= 2
        
        total_points += points

        for i in range(1, winning_nums + 1):
            copies[card_num + i] += copies[card_num]

    print(total_points)
    print(sum(copies))

