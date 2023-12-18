INPUT = 'input.txt'
# INPUT = '18.ex'

def parse_input_p1(file=INPUT):
    instructions = []
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()
            tokens = line.split()
            instructions.append((tokens[0], int(tokens[1])))
    return instructions

def parse_input_p2(file=INPUT):
    instructions = []
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()
            tokens = line.split()
            direction, length = hex_to_inst(tokens[2])
            instructions.append((direction, length))
    return instructions

def hex_to_inst(hex_str):
    # Hex str = "(#XXXXXX)"
    dir_map = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U',
    }
    
    length = int(hex_str[2:len(hex_str) - 2], base=16)
    direction = dir_map[hex_str[-2]]

    return direction, length

def points(instructions):
    dug = 0
    cur_row, cur_col = 0, 0
    coords = [(0, 0)]

    delta = {
        'D': (1, 0),
        'U': (-1, 0),
        'R': (0, 1),
        'L': (0, -1),
    }

    for direction, length in instructions:
        chg = delta[direction]
        dug += length
        cur_row += chg[0] * length
        cur_col += chg[1] * length
        coords.append((cur_row, cur_col))

    return dug, coords

def area(dug, coords):
    result = 0
    for i in range(len(coords)):
        prev = i - 1  # wraps to last point at -1 if at point 0
        nxt = i + 1 if i < len(coords) - 1 else 0

        horiz = coords[prev][1] - coords[nxt][1]
        vert = coords[i][0]
        result += horiz * vert

    result //= 2
    result += dug // 2 + 1
    return result


if __name__ == "__main__":
    instructions_p1 = parse_input_p1()
    dug_p1, coords_p1 = points(instructions_p1)

    instructions_p2 = parse_input_p2()
    dug_p2, coords_p2 = points(instructions_p2)

    print(area(dug_p1, coords_p1))
    print(area(dug_p2, coords_p2))

