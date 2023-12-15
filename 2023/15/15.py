import re

INPUT = 'input.txt'
# INPUT = '15.ex'

def parse_input(file=INPUT):
    with open(file) as f:
        return f.read().strip().replace('\n', '').split(',')

def hash_value(str):
    value = 0
    for c in str:
        value += ord(c)
        value *= 17
        value %= 256
    return value

if __name__ == "__main__":
    instructions = parse_input()

    # P1
    value = sum([hash_value(i) for i in instructions])
    print(value)

    # P2
    # Python dicts remember insertion order
    hashmap = [dict() for _ in range(256)]
    for inst in instructions:
        label, value = re.split(r'-|=', inst)
        bucket = hash_value(label)

        if value:
            hashmap[bucket][label] = int(value)
        elif label in hashmap[bucket]:
            del hashmap[bucket][label]

    focus_power = 0
    for box_num, box in enumerate(hashmap):
        for slot, length in enumerate(box.values()):
            focus_power += (box_num + 1) * (slot + 1) * length

    print(focus_power)



