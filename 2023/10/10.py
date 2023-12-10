from collections import deque

INPUT = 'input.txt'

def parse_input(file=INPUT):
    with open(file) as f:
        return [l.strip() for l in f.readlines()]

def neighbor_coords(row, col):
    north = (row - 1, col)
    south = (row + 1, col)
    east = (row, col + 1)
    west = (row, col - 1)

    return (north, south, east, west)

def neighbor_map(row, col):
    north, south, east, west = neighbor_coords(row, col)

    # Neighbors in sorted order to facilitate searching
    return {
        '|': (north, south),
        '-': (west, east),
        'L': (north, east),
        'J': (north, west),
        '7': (west, south),
        'F': (east, south),
    }

def convert_to_graph(lines):
    rows = len(lines)
    cols = len(lines[0])

    graph = dict()
    start_coords = (0, 0)
    for r, row in enumerate(lines):
        for c, val in enumerate(row):
            graph[(r, c)] = {
                'value': val,
                'neighbors': neighbor_map(r, c).get(val, [])
            }
            
            if val == 'S':
                start_coords = (r, c)

    return graph, start_coords

def populate_start_neighbors(start, graph):
    north, south, east, west = neighbor_coords(*start)

    if north in graph:
        north_val = graph[north]['value']
        if north_val in '|7F':
            graph[start]['neighbors'].append(north)

    if south in graph:
        south_val = graph[south]['value']
        if south_val in '|LJ':
            graph[start]['neighbors'].append(south)

    if east in graph:
        east_val = graph[east]['value']
        if east_val in '-J7':
            graph[start]['neighbors'].append(east)

    if west in graph:
        west_val = graph[west]['value']
        if west_val in '-LF':
            graph[start]['neighbors'].append(west)

def determine_start_char(start, neighbors):
    for char, ns in neighbor_map(*start).items():
        if ns == tuple(sorted(neighbors)):
            return char


if __name__ == "__main__":
    lines = parse_input()
    graph, start = convert_to_graph(lines)
    populate_start_neighbors(start, graph)

    # Part 1
    # Simple BFS, count time until we cycle

    dist = 0
    queue = deque([start])
    visited = set()
    while queue:
        cur = queue.popleft()
        visited.add(cur)

        for neighbor in graph[cur]['neighbors']:
            if neighbor not in visited:
                queue.append(neighbor)

        dist += 1

    print(dist // 2)

    # Part 2
    # Iterate over chars horizontally
    # Maintain state: are we inside loop? is area above, or below, inside?
    # When we hit certain chars, update state accordingly
    # Need to know above/below so we can update "enclosed" state when we
    # hit a 7, J, F, L
    # Ignore all chars that are not part of the loop (set them to '.')

    enclosed = set()
    for r, row in enumerate(lines):
        # True if currently inside loop (enclosed)
        inside_loop = False

        # None if we are outside loop
        # True if area above current row is enclosed
        # False if area below current row is enclosed
        enclosed_above = None

        for col, cur_char in enumerate(row):
            # Only need to update state if we are at loop cell
            if (r, col) in visited:
                if cur_char == 'S':
                    cur_char = determine_start_char(start, graph[start]['neighbors'])

                match cur_char:
                    case '|':
                        inside_loop = not inside_loop

                    case 'L':
                        enclosed_above = True

                    case 'F':
                        enclosed_above = False

                    case '7':
                        if enclosed_above:
                            inside_loop = not inside_loop
                        enclosed_above = None

                    case 'J':
                        if not enclosed_above:
                            inside_loop = not inside_loop 
                        enclosed_above = None

            else:
                # Add cell to set if we are inside loop
                # Note: cells on loop are not enclosed
                if inside_loop:
                    enclosed.add((r, col))

    print(len(enclosed))

