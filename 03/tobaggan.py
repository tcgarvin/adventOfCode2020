from functools import reduce

def solve_part_1(puzzle_input):
    section_width = len(puzzle_input[0])
    x = 0
    trees = 0
    for line in puzzle_input:
        if line[x % section_width] == "#":
            trees += 1

        x += 3

    return trees

def solve_part_2(puzzle_input):
    section_width = len(puzzle_input[0])
    puzzle_height = len(puzzle_input)

    totals = []
    for right, down in ((1,1),(3,1),(5,1),(7,1),(1,2)):
        x = 0
        trees = 0
        for i in range(0, puzzle_height, down):
            if puzzle_input[i][x % section_width] == "#":
                trees += 1
            x += right

        totals.append(trees)

    return reduce(lambda a,b: a * b, totals)

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(line.strip())
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")