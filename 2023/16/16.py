import collections
from enum import Enum

INPUT = 'input.txt'
# INPUT = '16.ex'

class Direction(Enum):
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3

def parse_data(file=INPUT):
    grid = []
    with open(file) as f:
        grid = [[c for c in line.strip()] for line in f.readlines()]
    return grid

def get_next(row, col, val, direction):
    match val:
        case '.':
            match direction:
                case Direction.NORTH:
                    return [((row - 1, col), direction)]
                case Direction.SOUTH:
                    return [((row + 1, col), direction)]
                case Direction.WEST:
                    return [((row, col - 1), direction)]
                case Direction.EAST:
                    return [((row, col + 1), direction)]

        case '|':
            match direction:
                case Direction.NORTH:
                    return [((row - 1, col), direction)]
                case Direction.SOUTH:
                    return [((row + 1, col), direction)]
                case Direction.EAST | Direction.WEST:
                    return [
                        ((row - 1, col), Direction.NORTH),
                        ((row + 1, col), Direction.SOUTH),
                    ]

        case '-':
            match direction:
                case Direction.NORTH | Direction.SOUTH:
                    return [
                        ((row, col - 1), Direction.WEST),
                        ((row, col + 1), Direction.EAST),
                    ]
                case Direction.WEST:
                    return [((row, col - 1), Direction.WEST)]
                case Direction.EAST:
                    return [((row, col + 1), Direction.EAST)]

        case '/':
            match direction:
                case Direction.NORTH:
                    return [((row, col + 1), Direction.EAST)]
                case Direction.SOUTH:
                    return [((row, col - 1), Direction.WEST)]
                case Direction.WEST:
                    return [((row + 1, col), Direction.SOUTH)]
                case Direction.EAST:
                    return [((row - 1, col), Direction.NORTH)]

        case '\\':
            match direction:
                case Direction.NORTH:
                    return [((row, col - 1), Direction.WEST)]
                case Direction.SOUTH:
                    return [((row, col + 1), Direction.EAST)]
                case Direction.WEST:
                    return [((row - 1, col), Direction.NORTH)]
                case Direction.EAST:
                    return [((row + 1, col), Direction.SOUTH)]

def edge_cells(grid):
    rows = len(grid)
    cols = len(grid[0])

    cells = [
        # Upper left corner
        ((0, 0), Direction.EAST),

        # Upper right corner
        ((0, cols - 1), Direction.WEST),

        # Lower left corner
        ((rows - 1, 0), Direction.EAST),

        # Lower right corner
        ((rows - 1, cols - 1), Direction.WEST),
    ]

    for row in range(rows):
        if row == 0:
            cells += [
                ((row, col), Direction.SOUTH)
                for col in range(0, cols)
            ]
        elif row == rows - 1:
            cells += [
                ((row, col), Direction.NORTH)
                for col in range(0, cols)
            ]
        else:
            cells += [
                ((row, col), Direction.EAST if col == 0 else Direction.WEST)
                for col in (0, cols - 1)
            ]

    return cells


if __name__ == "__main__":
    grid = parse_data()
    rows = len(grid)
    cols = len(grid[0])

    max_energized = float('-inf')
    for start in edge_cells(grid):
        queue = collections.deque([start])
        seen = set()  # use to avoid repeating routes
        energized = set()  # use to track cells visited (direction agnostic)

        while queue:
            (row, col), direction = queue.popleft()

            # Skip if outside grid or route has been done before
            if (
                not (0 <= row < rows and 0 <= col < cols) or
                (row, col, direction) in seen
            ):
                continue

            energized.add((row, col))
            seen.add((row, col, direction))
            val = grid[row][col]
            nxt = get_next(row, col, val, direction)
            queue.extend(nxt)
        
        max_energized = max(max_energized, len(energized))

        # P1
        if start == ((0, 0), Direction.EAST):
            print(len(energized))

    # P2
    print(max_energized)

