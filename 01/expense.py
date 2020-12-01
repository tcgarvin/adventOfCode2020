from itertools import combinations

def solve_part_1(puzzle_input):
    for a,b in combinations(puzzle_input, 2):
        if a + b == 2020:
            return a * b
    return ""

def solve_part_2(puzzle_input):
    for a,b,c in combinations(puzzle_input, 3):
        if a + b + c == 2020:
            return a * b * c
    return ""

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(int(line))
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")