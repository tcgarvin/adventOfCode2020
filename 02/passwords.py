import re

LINE_RE = re.compile("""
    ^
    ([0-9]+)
    -
    ([0-9]+)
    [ ]
    ([a-z])
    :[ ]
    ([a-z]+)
    $
""", re.X)


def solve_part_1(puzzle_input):
    valid = 0
    for entry in puzzle_input:
        fewest = int(entry[0])
        most = int(entry[1])
        letter = entry[2]
        password = entry[3]

        count = password.count(letter)
        if count >= fewest and count <= most:
            valid += 1

        #print(fewest, most, letter, password, count, valid)

    return valid

def solve_part_2(puzzle_input):
    valid = 0
    for entry in puzzle_input:
        pos1 = int(entry[0]) - 1
        pos2 = int(entry[1]) - 1
        letter = entry[2]
        password = entry[3]

        if (password[pos1] == letter) != (password[pos2] == letter):
            valid += 1

        #print(pos1, pos2, letter, password, valid)

    return valid

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(LINE_RE.match(line).groups())
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")