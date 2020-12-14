from copy import deepcopy
from rich import print

DIRECTIONS = ((1,0), (1,1), (0,1), (-1,1), (-1,0), (-1, -1), (0, -1), (1, -1))

def display_grid(grid):
    for row in grid:
        print("".join(row))
    print("")


def tick(grid):
    next_grid = deepcopy(grid)
    has_changed = False
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            num_occupied = 0
            for di, dj in DIRECTIONS:
                if grid[i + di][j + dj] == "#":
                    num_occupied += 1

            if grid[i][j] == "L" and num_occupied == 0:
                next_grid[i][j] = "#"
                has_changed = True

            elif grid[i][j] == "#" and num_occupied >= 4:
                next_grid[i][j] = "L"
                has_changed = True
            
    return (next_grid, has_changed)

def tick2(grid):
    maxI = len(grid)    - 1
    maxJ = len(grid[0]) - 1

    next_grid = deepcopy(grid)
    has_changed = False
    for i in range(1, maxI):
        for j in range(1, maxJ):
            num_occupied = 0
            for di, dj in DIRECTIONS:
                for m in range(1,200):
                    checkI = i + di * m
                    checkJ = j + dj * m

                    if checkI < 1 or checkJ < 1 or checkI > maxI or checkJ > maxJ:
                        break

                    x = grid[checkI][checkJ]
                    if x == "#":
                        num_occupied += 1
                        break

                    elif x == "L":
                        break

            if grid[i][j] == "L" and num_occupied == 0:
                next_grid[i][j] = "#"
                has_changed = True

            elif grid[i][j] == "#" and num_occupied >= 5:
                next_grid[i][j] = "L"
                has_changed = True
            
    return (next_grid, has_changed)

def solve(puzzle_input, tick_func):
    input_width = len(puzzle_input[0])
    grid_width = input_width + 2

    grid = []
    grid.append(["."] * grid_width)
    for row in puzzle_input:
        grid.append(["."] + list(row) + ["."])
    grid.append(["."] * grid_width)

    has_changed = True
    display_grid(grid)
    while has_changed is True:
        grid, has_changed = tick_func(grid)
        display_grid(grid)

    total_occupied = 0
    for row in grid:
        total_occupied += row.count("#")

    return total_occupied

def solve_part_1(puzzle_input):
    return solve(puzzle_input, tick)

def solve_part_2(puzzle_input):
    return solve(puzzle_input, tick2)

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