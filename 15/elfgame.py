from collections import defaultdict

from rich import print
from rich.progress import track

def solve(first_numbers, ith):
    spoken = []
    turns_spoken = defaultdict(list)
    for i in track(range(ith)):
        if i < len(first_numbers):
            number = first_numbers[i]
            spoken.append(number)
            turns_spoken[number].append(i)
            continue

        last_spoken = spoken[-1]

        times_spoken = turns_spoken[last_spoken]

        how_long_ago = 0
        if len(times_spoken) > 1:
            how_long_ago = i - times_spoken[-2] - 1

        spoken.append(how_long_ago)
        turns_spoken[how_long_ago].append(i)

    return spoken[ith - 1]

def solve_part_1(first_numbers):
    return solve(first_numbers, 2020)

def solve_part_2(first_numbers):
    return solve(first_numbers, 30000000)

if __name__ == "__main__":
    puzzle_input = [13,0,10,12,1,5,8]

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")