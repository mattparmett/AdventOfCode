INPUT = 'input.txt'
# INPUT = '14.ex'

def parse_data(file=INPUT):
    lines = []
    with open(file) as f:
        lines = [[c for c in line] for line in f.read().strip().split('\n')]
    return lines

def roll_col(col, grid):
    assert(0 <= col < len(grid[0]))

    empty_row = 0
    for row in range(len(grid)):
        match grid[row][col]:
            case '#':
                empty_row = row + 1

            case 'O':
                # Move up to highest empty_row
                if empty_row < row:
                    grid[empty_row][col] = 'O'
                    grid[row][col] = '.'
                empty_row += 1

            case '.':
                pass

    return grid

def roll_grid(grid):
    for col in range(len(grid[0])):
        grid = roll_col(col, grid)
    return grid

def rotate_90(grid):
    """
    Rotates grid 90 degrees clockwise.
    """
    return [list(x) for x in list(zip(*grid[::-1]))]


def spin_cycle(grid):
    """
    Performs 1 "spin cycle": roll north,
    west, south, east.
    """
    for _ in range(4):
        grid = roll_grid(grid)
        grid = rotate_90(grid)
    return grid

def north_load(grid):
    rows = len(grid)
    load = 0
    for r, row in enumerate(grid):
        rocks = sum(v == 'O' for v in row)
        load += rocks * (rows - r)
    return load


if __name__ == "__main__":
    grid = parse_data()

    # P1
    p1_grid = roll_grid(grid)
    p1_load = north_load(p1_grid)
    print(p1_load)

    # P2
    p2_grid = grid

    # Grid stabilizes somewhere 
    # close to 1,000 spins
    spins = 1_000
    for _ in range(spins):
        p2_grid = spin_cycle(p2_grid)

    p2_load = north_load(p2_grid)
    print(p2_load)

