from functools import reduce
from rich import print

def solve_part_1(puzzle_input):
    total = 0
    for group in puzzle_input:
        any_answered = reduce(lambda a,b: a | b, group)
        total += len(any_answered)

    return total


def solve_part_2(puzzle_input):
    total = 0

    for group in puzzle_input:
        all_answered = reduce(lambda a,b: a & b, group)
        total += len(all_answered)

    return total


def get_puzzle_input():
    puzzle_input = []
    group = []
    puzzle_input.append(group)
    with open("input.txt") as input_txt:
        for line in input_txt:
            if len(line.strip()) == 0:
                group = []
                puzzle_input.append(group)
            else:
                group.append(set(line.strip()))

    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")