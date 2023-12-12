from functools import cache

INPUT = 'input.txt'
# INPUT = '12.ex'

def parse_input(file=INPUT, folds=1):
    lines = []
    with open(file) as f:
        for line in f.readlines():
            tokens = line.strip().split()
            springs = '?'.join([tokens[0] for _ in range(folds)])
            blocks = [int(t) for t in tokens[1].split(',')] * folds
            lines.append((tuple(springs), tuple(blocks)))
    return lines

def handle_dot(springs, blocks):
    """
    Called when the first spring is a '.'.

    We simply want to skip this spring
    and move forward with the same blocks.
    """
    return solve(springs[1:], blocks)

def handle_hash(springs, blocks):
    """
    Called when the first spring is a #
    (or we are assuming that ? is a #),
    meaning we are at the start of a new block.

    Check that this block is valid, and if so,
    move to analyze the next block.  If not,
    return 0, since there are no arrangements
    that contain this block.
    """
    block_size = blocks[0]

    # Check: can't have block longer than num springs
    if block_size > len(springs):
        return 0

    # Check: block must be contiguous
    # (i.e. no operational springs in block)
    if '.' in springs[:block_size]:
        return 0

    # Check: must have operational spring at
    # exactly the end of the block (can be '.' or '?',
    # which can be mapped to '.')
    if len(springs) > block_size and springs[block_size] == '#':
        return 0

    # If all checks pass, this is a valid block.
    # Move past this block to the next one.
    return solve(springs[block_size + 1:], blocks[1:])

@cache  # req. for part 2 given large sizes
def solve(springs, blocks):
    """
    Base case: no more springs

    This is a valid arrangement if there
    are no more contiguous blocks; otherwise
    there are no valid arrangements.
    """
    if len(springs) == 0:
        return len(blocks) == 0

    """
    Base case: no more blocks

    This is a valid arrangement if there are
    no more '#' springs (otherwise we would
    need another block to house those).

    Otherwise, there are 0 possible arrangements.

    Note: '?'s are OK since we can map those
    to '.'s and maintain the validity of the
    arrangement.
    """
    if len(blocks) == 0:
        return '#' not in springs

    arrangements = 0

    match springs[0]:
        case '.':
            arrangements = handle_dot(springs, blocks)

        case '#':
            arrangements = handle_hash(springs, blocks)

        # ? can be either dot or hash
        case '?':
            arrangements = (
                handle_dot(springs, blocks) + 
                handle_hash(springs, blocks)
            )

    return arrangements


if __name__ == "__main__":
    p1_data = parse_input()
    p1_result = sum([
        solve(springs, blocks)
        for springs, blocks in p1_data
    ])
    print(p1_result)

    p2_data = parse_input(folds=5)
    p2_result = sum([
        solve(springs, blocks)
        for springs, blocks in p2_data
    ])
    print(p2_result)

