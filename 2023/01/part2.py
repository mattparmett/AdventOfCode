"""
Advent of Code
Puzzle 1
Part 2
"""

CALIBRATION_FILE = "calibration.txt"
DIGIT_WORDS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def get_digit_word(s):
    for word, value in DIGIT_WORDS.items():
        if word == s[:len(word)]:
            return value

    return None

if __name__ == "__main__":
    calibration_sum = 0

    with open(CALIBRATION_FILE) as f:
        for line in f:
            line = line.strip()
            left = None
            right = None

            i = 0
            while left is None:
                left = line[i] if line[i].isdigit() else get_digit_word(line[i:])
                i += 1

            i = len(line) - 1
            while right is None:
                right = line[i] if line[i].isdigit() else get_digit_word(line[i:])
                i -= 1

            calibration_sum += int(left + right)

    print(calibration_sum)

