from heapq import heappush, heappop

INPUT = 'input.txt'
# INPUT = '17.ex'

def parse_data(file=INPUT):
    with open(file) as f:
        return [[int(c) for c in line.strip()] for line in f.readlines()]

def solve(grid, min_moves=0, max_moves=float('inf')):
    rows = len(grid)
    cols = len(grid[0])

    def cell_valid(row, col):
        return 0 <= row < rows and 0 <= col < cols

    visited = set()
    queue = [(
        0,      # heat loss
        0,      # current row
        0,      # current col
        0,      # delta row (move)
        0,      # delta col (move)
        0,      # number of consecutive moves
    )]

    while queue:
        heat_loss, row, col, d_row, d_col, num_moves = heappop(queue)

        """
        If the end cell is at the top of the priority queue, and we
        are here on a valid path (we've met the number of minimum moves),
        we have found the shortest path and are done.
        """
        if row == rows - 1 and col == cols - 1 and num_moves > min_moves:
            return heat_loss

        """
        If we've already visited this cell from this
        direction with the same number of moves,
        it will not lead us to a different path/heat loss;
        so skip it by tracking in a visited set.
        """
        visited_key = (
            row,
            col,
            d_row,
            d_col,
            num_moves,
        )

        if visited_key in visited:
            continue

        visited.add(visited_key)

        below_min_moves = num_moves <= min_moves
        at_moves_limit = num_moves == max_moves
        at_start_cell = (row, col) == (0, 0)

        """
        Move forward.

        We can move "forward" if we are below the max moves
        limit.

        Note: we have no "forward" direction if we're at the
        start cell, so need to make sure we are not there
        to execute a forward move.
        """
        if not at_moves_limit and not at_start_cell:
            new_row = row + d_row
            new_col = col + d_col

            if cell_valid(new_row, new_col):
                new_heat_loss = heat_loss + grid[new_row][new_col]
                queue_key = (
                    new_heat_loss,
                    new_row,
                    new_col,
                    d_row,
                    d_col,
                    num_moves + 1
                )
                heappush(queue, queue_key)

        """
        Check all possible moves, and add valid moves to the queue.
        If we are below the minimum number of moves, we are only allowed
        to move forward, which we already handled above, so skip this block.

        Check if we are at start cell to make sure we evaluate all moves
        from the start.
        """
        if (not below_min_moves) or at_start_cell:
            # Check all neighbors for valid moves and add to queue
            deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for delta in deltas:
                # Already handled forward move, and can't move backward
                if delta == (d_row, d_col) or delta == (-d_row, -d_col):
                    continue

                new_row = row + delta[0]
                new_col = col + delta[1]
                if cell_valid(new_row, new_col):
                    new_heat_loss = heat_loss + grid[new_row][new_col]
                    queue_key = (
                        new_heat_loss,
                        new_row,
                        new_col,
                        delta[0],
                        delta[1],
                        1
                    )
                    heappush(queue, queue_key)

if __name__ == "__main__":
    grid = parse_data()

    p1 = solve(grid, 0, 3)
    print(p1)

    p2 = solve(grid, 3, 10)
    print(p2)
