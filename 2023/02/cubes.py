INPUT_FILE = 'input.txt'
AVAILABLE = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

def parse_game_input(line):
    tokens = line.split(':')
    game_id = tokens[0].split()[-1]
    reveals = list()  # will be list of dicts {color: amt}

    for reveal in tokens[1].split(';'):
        reveal = reveal.strip()
        cubes = [c.strip() for c in reveal.split(',')]
        result = dict()

        for cube in cubes:
            cube_tokens = cube.split()
            amt = cube_tokens[0]
            color = cube_tokens[1].lower()
            result[color] = int(amt)

        reveals.append(result)

    return game_id, reveals

def parse_input(input_file=INPUT_FILE):
    games = dict()
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            game_id, reveals = parse_game_input(line)
            games[game_id] = reveals
    return games

def max_cubes(reveals):
    maximums = {
        'red': float('-inf'),
        'green': float('-inf'),
        'blue': float('-inf'),
    }

    for reveal in reveals:
        for color in maximums:
            if color in reveal:
                maximums[color] = max(maximums[color], reveal[color])

    return maximums

def game_possible(reveals):
    maximums = max_cubes(reveals)
    return all([
        maximums[color] <= AVAILABLE[color]
        for color in maximums
    ])

def power(cubes):
    product = 1
    for amt in cubes.values():
        product *= amt
    return product

if __name__ == "__main__":
    # Part 1
    games = parse_input()
    possible_game_id_sum = sum([
        int(game_id)
        for game_id, reveals in games.items()
        if game_possible(reveals)
    ])
    print('Part 1:', possible_game_id_sum)

    # Part 2
    power_of_minimums = sum([
        power(max_cubes(reveals))
        for reveals
        in games.values()
    ])
    print('Part 2:', power_of_minimums)


