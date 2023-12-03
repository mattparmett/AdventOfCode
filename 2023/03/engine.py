from math import prod

def is_symbol(c):
    return all([
        not c.isdigit(),
        c != '.',
    ])

def read_input(filename):
    with open(filename) as f:
        return [[c for c in line.strip()] for line in f.readlines()]

def get_part_num_idxs(row_idx, init_idx):
    start = init_idx
    end = init_idx
    row = matrix[row_idx]

    while start >= 0 and row[start].isdigit():
        start -= 1

    while end < len(row) and row[end].isdigit():
        end += 1

    return (start + 1, end - 1)

def get_num(row_idx, start, end):
    row = matrix[row_idx]
    return int(''.join(row[start:end + 1]))

def mark_num_used(row_idx, start_idx, end_idx):
    row = matrix[row_idx]
    while start_idx <= end_idx:
        row[start_idx] = '.'
        start_idx += 1

def neighbors(row, col):
    return [
        (row - 1, col - 1),
        (row - 1, col),
        (row - 1, col + 1),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row + 1, col + 1),
    ]


if __name__ == "__main__":
    # Iterate through matrix.  When see symbol, add all numbers around it,
    # and replace each number with periods after adding
    matrix = read_input('input.txt')
    p1_result = 0
    p2_result = 0
    for row_idx, row in enumerate(matrix):
        for col_idx, c in enumerate(row):
            if is_symbol(c):
                adj_nums = list()
                for (n_row, n_col) in neighbors(row_idx, col_idx):
                    if matrix[n_row][n_col].isdigit():
                        num_start, num_end = get_part_num_idxs(n_row, n_col)
                        num = get_num(n_row, num_start, num_end)
                        p1_result += num
                        if c == '*':
                            adj_nums.append(num)
                        mark_num_used(n_row, num_start, num_end)

                if c == '*' and len(adj_nums) == 2:
                    p2_result += prod(adj_nums)

    print(p1_result)
    print(p2_result)

