from itertools import combinations

from rich import print

def solve_part_1(puzzle_input):
    for i in range(25, len(puzzle_input)):
        is_sum_of_previous = False
        for a,b in combinations(puzzle_input[i-25:i], 2):
            is_sum_of_previous |= a + b == puzzle_input[i]
            if is_sum_of_previous:
                continue

        if not is_sum_of_previous:
            return puzzle_input[i]

    return "Not found"

def solve_part_2(puzzle_input, invalid_number):
    for i in range(len(puzzle_input)):
        for j in range(i + 1, len(puzzle_input)):
            contiguous_range = puzzle_input[i:j+1]
            total = sum(contiguous_range)
            if total == invalid_number:
                return min(contiguous_range) + max(contiguous_range)
            elif total > invalid_number:
                break

    return "Not found"

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

    answer_2 = solve_part_2(puzzle_input, answer_1)
    print(f"Part 2: {answer_2}")