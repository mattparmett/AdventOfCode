INPUT = 'input.txt'
# INPUT = '09.ex'

def parse_input(file=INPUT):
    lines = []
    with open(file) as f:
        lines = [line.strip() for line in f]

    seqs = []
    for line in lines:
        seqs.append([int(n) for n in line.split()])

    return seqs

def gradient(seq):
    gradient = []
    for i in range(1, len(seq)):
        gradient.append(seq[i] - seq[i - 1])
    return gradient

def gradient_pyramid(seq):
    gradients = [seq]
    while sum(seq):
        seq = gradient(seq)
        gradients.append(seq)
    return gradients

def extrapolate(seq):
    pyramid = gradient_pyramid(seq)
    pyramid[-1].append(0)
    pyramid[-1].insert(0, 0)

    for i in range(len(pyramid) - 2, -1, -1):
        right_val = pyramid[i][-1] + pyramid[i + 1][-1]
        left_val = pyramid[i][0] - pyramid[i + 1][0]
        pyramid[i].append(right_val)
        pyramid[i].insert(0, left_val)


    return pyramid[0][-1], pyramid[0][0]

if __name__ == "__main__":
    seqs = parse_input()

    p1 = 0
    p2 = 0
    for seq in seqs:
        v1, v2 = extrapolate(seq)
        p1 += v1
        p2 += v2

    print(p1)
    print(p2)

