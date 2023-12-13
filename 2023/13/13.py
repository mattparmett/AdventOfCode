INPUT = 'input.txt'
# INPUT = '13.ex'

def parse_input(file=INPUT):
    patterns = []
    with open(file) as f:
        data = f.read()
        patterns = [p.strip().split() for p in data.split('\n\n')]
    
    return patterns

def horiz_mirror(pattern, max_diff=0):
    for row in range(1, len(pattern)):
        # top = upper portion of "mirrored" (i.e. above current pivot)
        top = pattern[:row][::-1]  # need to reverse top for "mirroring"

        # bottom = lower portion of "mirrored" (i.e. below current pivot)
        bottom = pattern[row:]

        # diffs = number of diffs across all top/bottom rows in "mirrored"
        diffs = 0
        for top_row, bot_row in zip(top, bottom):
            for col in range(len(pattern[0])):
                diffs += top_row[col] != bot_row[col]

        if diffs == max_diff:
            return row

    return 0

def vert_mirror(pattern, max_diff=0):
    pattern_T = list(zip(*pattern))
    return horiz_mirror(pattern_T, max_diff)

if __name__ == "__main__":
    patterns = parse_input()

    p1 = 0
    for pattern in patterns:
        p1 += 100 * horiz_mirror(pattern)
        p1 += vert_mirror(pattern)

    print(p1)

    p2 = 0
    for pattern in patterns:
        p2 += 100 * horiz_mirror(pattern, 1)
        p2 += vert_mirror(pattern, 1)

    print(p2)

