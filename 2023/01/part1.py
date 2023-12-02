"""
Advent of Code
Puzzle 1
"""

CALIBRATION_FILE = "calibration.txt"

if __name__ == "__main__":
    calibration_sum = 0

    with open(CALIBRATION_FILE) as f:
        for line in f:
            line = line.strip()
            left = None
            right = None

            i = 0
            while left is None:
                if line[i].isdigit():
                    left = line[i]
                i += 1

            i = len(line) - 1
            while right is None:
                if line[i].isdigit():
                    right = line[i]
                i -= 1

            calibration_sum += int(left + right)

    print(calibration_sum)

