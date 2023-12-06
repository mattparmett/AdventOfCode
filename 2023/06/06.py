from math import prod as product

INPUT = "input.txt"

def parse_input_p1(file=INPUT):
    lines = []
    with open(file) as f:
        lines = f.readlines()

    _, *times = lines[0].split()
    _, *dists = lines[1].split()

    return zip(
        [int(t) for t in times], 
        [int(d) for d in dists]
    )


def parse_input_p2(file=INPUT):
    lines = []
    with open(file) as f:
        lines = f.readlines()

    _, *times = lines[0].split()
    _, *dists = lines[1].split()

    return (
        int(''.join(times)),
        int(''.join(dists))
    )


if __name__ == "__main__":
    # P1

    races = parse_input_p1()
    p1_result = []

    for time, min_dist in races:
        winning_speeds = 0

        for speed in range(time + 1):
            remaining = time - speed
            dist_traveled = remaining * speed

            if dist_traveled > min_dist:
                winning_speeds += 1

        p1_result.append(winning_speeds)

    print(product(p1_result))

    # P2

    time, min_dist = parse_input_p2()
    p2_result = 0

    for speed in range(time + 1):
        remaining = time - speed
        dist_traveled = remaining * speed

        if dist_traveled > min_dist:
            p2_result += 1

    print(p2_result)

