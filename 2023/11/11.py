INPUT = 'input.txt'
# INPUT = '11.ex'

def load_input(file=INPUT):
    num_cols = 0
    coords = set()
    empty_rows = set()
    populated_cols = set()

    with open(file) as f:
        for row, line in enumerate(f.readlines()):
            if not num_cols:
                num_cols = len(line)

            empty_row = True

            for col, val in enumerate(line.strip()):
                if val != '.':
                    empty_row = False
                    populated_cols.add(col)

                if val == '#':
                    coords.add((row, col))

            if empty_row:
                empty_rows.add(row)

    empty_cols = set(range(num_cols)) - populated_cols
    return coords, empty_rows, empty_cols

def expand_coord(coord, blank_rows, blank_cols, factor=2):
    """
    Map a coordinate pair to its expanded equivalent.
    """
    row, col = coord

    empty_rows_before = len([r for r in blank_rows if r < row])
    empty_cols_before = len([c for c in blank_cols if c < col])

    return (
        row + (factor - 1) * empty_rows_before,
        col + (factor - 1) * empty_cols_before,
    )

def distance(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

def total_distance(coords):
    total_dist = 0
    pairs = set()

    for cur_coord in coords:
        for other_coord in coords:
            if any([
                cur_coord == other_coord,
                (cur_coord, other_coord) in pairs,
                (other_coord, cur_coord) in pairs,
            ]):
                continue

            total_dist += distance(other_coord, cur_coord)
            pairs.add((cur_coord, other_coord))

    return total_dist


if __name__ == "__main__":
    galaxy_coords, blank_rows, blank_cols = load_input()

    p1_coords = {
        expand_coord(coord, blank_rows, blank_cols)
        for coord in galaxy_coords
    }
    print(total_distance(p1_coords))

    p2_coords = {
        expand_coord(coord, blank_rows, blank_cols, 1_000_000)
        for coord in galaxy_coords
    }
    print(total_distance(p2_coords))

