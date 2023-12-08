INPUT = 'input.txt'
# INPUT = '08.ex'

def parse_input(file=INPUT):
    lines = []
    with open(file) as f:
        lines = [l.strip() for l in f.readlines()]

    directions = lines[0]

    nodes = dict()
    for line in lines[2:]:
        start, neighbors = line.split(' = ')
        left, right = neighbors.replace('(', '').replace(')', '').split(', ')
        nodes[start] = (left.strip(), right.strip())

    return directions, nodes

def process_node(nodes, directions, start, condition):
    steps = 0
    while not condition(start):
        direction = directions[steps % len(directions)]
        next_idx = int(direction == 'R')
        start = nodes[start][next_idx]
        steps += 1

    return steps

def gcd(m, n):
    """
    Finds greatest common divisor using Euclidean algo
    """
    while n != 0:
        tmp = n
        n = m % n
        m = tmp

    return m

def lcm(m, n):
    return (m * n) // gcd(m, n)

def find_lcm(nums):
    result = 1
    for num in nums:
        result = lcm(result, num)
    return result


if __name__ == "__main__":
    directions, nodes = parse_input()

    # P1
    steps = process_node(nodes, directions, 'AAA', lambda n: n == 'ZZZ')
    print(steps)

    # P2
    # Find time when each node arrives at endswith Z
    # Then find least common multiple of those times
    steps = [
        process_node(nodes, directions, node, lambda n: n.endswith('Z'))
        for node in nodes
        if node.endswith('A')
    ]
    
    print(find_lcm(steps))
