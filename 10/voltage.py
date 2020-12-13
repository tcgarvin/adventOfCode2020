from collections import defaultdict
from itertools import chain, combinations

from rich import print

def solve_part_1(puzzle_input):
    distribution = defaultdict(int)
    voltage_ladder = sorted(puzzle_input + [0])
    for i in range(1,len(voltage_ladder)):
        difference = voltage_ladder[i] - voltage_ladder[i - 1]
        distribution[difference] += 1

    distribution[3] += 1

    return distribution[1] * distribution[3]

def powerset(iterable):
    """This recipe is from itertools docs"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def is_valid_combination(combination):
    for i in range(1, len(combination)):
        if combination[i] - combination[i-1] > 3:
            return False
        
    return True

def count_valid_combinations(voltage_ladder):
    #print(voltage_ladder)
    if len(voltage_ladder) <= 2:
        #print(1)
        return 1

    count = 0
    for combination in powerset(voltage_ladder[1:-1]):
        candidate = [voltage_ladder[0]] + list(sorted(combination)) + [voltage_ladder[-1]]
        if is_valid_combination(candidate):
            count += 1

    #print(count)

    return count

def solve_part_2(puzzle_input):
    #print(sorted(puzzle_input))
    sorted_input = sorted(puzzle_input)
    voltage_ladder = [0] + sorted_input + [sorted_input[-1] + 3]
    total_possibilities = 1
    current_group = []
    for i in range(len(voltage_ladder)):
        if len(current_group) == 0:
            current_group.append(voltage_ladder[i])
        
        elif voltage_ladder[i] - voltage_ladder[i-1] < 3:
            current_group.append(voltage_ladder[i])

        elif voltage_ladder[i] - voltage_ladder[i-1] == 3:
            total_possibilities *= count_valid_combinations(current_group)
            current_group = [voltage_ladder[i]]

        else:
            raise Exception("Saw gap greater than 3")

    print(current_group)
    return total_possibilities

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