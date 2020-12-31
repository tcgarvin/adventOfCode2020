from rich import print

from collections import defaultdict

STEP_INDEX = {
    "ne": (0,1),
    "e": (1,0),
    "se": (1,-1),
    "sw": (0, -1),
    "w": (-1, 0),
    "nw": (-1, 1)
}

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            instructions = []
            prefix = ""
            for char in line.strip():
                if char not in ("e", "w"):
                    assert prefix == ""
                    prefix = char
                else:
                    instruction = prefix + char
                    instructions.append(instruction)
                    prefix = ""

            puzzle_input.append(instructions)

    return puzzle_input

def solve_part_1(puzzle_input):
    grid = defaultdict(bool)

    for instructions in puzzle_input:
        x = 0
        y = 0
        for step in instructions:
            dx, dy = STEP_INDEX[step]
            x += dx
            y += dy

        grid[(x,y)] = not grid[(x,y)]

    return sum(grid.values()), grid

def solve_part_2(grid):
    for day in range(100):
        #print(f"Day {day}: {sum(grid.values())}")
        to_flip = set()
        white_tiles_to_check = defaultdict(int)
        for coordinates, is_black in grid.items():
            if not is_black:
                continue

            #print(f"Examining {coordinates}")

            x, y = coordinates

            adjacent_black_tiles = 0
            for dx, dy in STEP_INDEX.values():
                adjacent_coordinates = (x + dx, y + dy)
                adjacent_tile_is_black = grid.get(adjacent_coordinates, False)
                if adjacent_tile_is_black:
                    adjacent_black_tiles += 1
                    #print(f"Adjacent {adjacent_coordinates} makes {adjacent_black_tiles}.")
                else:
                    white_tiles_to_check[adjacent_coordinates] += 1

            if adjacent_black_tiles == 0 or adjacent_black_tiles > 2:
                to_flip.add(coordinates)

        for coordinates, num_black_adjacent in white_tiles_to_check.items():
            if num_black_adjacent == 2:
                to_flip.add(coordinates)

        for coordinates in to_flip:
            grid[coordinates] = not grid[coordinates]

    return sum(grid.values())

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1, grid = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(grid)
    print(f"Part 2: {answer_2}")