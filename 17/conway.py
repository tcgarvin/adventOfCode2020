from rich import print

OFFSETS = (-1, 0, 1)

def tick(active_grid):
    next_grid = set()
    inactive_cells_to_check = set()
    for key in active_grid:
        x,y,z = key
        active_neighbors = 0
        for dx in OFFSETS:
            for dy in OFFSETS:
                for dz in OFFSETS:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue
                    neighbor_coordinates = (x+dx, y+dy, z+dz)
                    neighbor_is_active = neighbor_coordinates in active_grid
                    if neighbor_is_active:
                        active_neighbors += 1
                    else:
                        inactive_cells_to_check.add(neighbor_coordinates)

        if active_neighbors in (2,3):
            next_grid.add(key)

    #print(len(inactive_cells_to_check))
    for key in inactive_cells_to_check:
        x,y,z = key
        active_neighbors = 0
        for dx in OFFSETS:
            for dy in OFFSETS:
                for dz in OFFSETS:
                    neighbor_coordinates = (x+dx, y+dy, z+dz)
                    neighbor_is_active = neighbor_coordinates in active_grid
                    if neighbor_is_active:
                        active_neighbors += 1

        if active_neighbors == 3:
            next_grid.add(key)

    return next_grid

def solve_part_1(puzzle_input):
    grid = set()

    for x in range(len(puzzle_input[0])):
        for y in range(len(puzzle_input)):
            if puzzle_input[y][x]:
                grid.add((x,y,0))

    for _ in range(6):
        #print(grid)
        grid = tick(grid)

    return len(grid)


def tick4d(active_grid):
    next_grid = set()
    inactive_cells_to_check = set()
    for key in active_grid:
        w,x,y,z = key
        active_neighbors = 0
        for dw in OFFSETS:
            for dx in OFFSETS:
                for dy in OFFSETS:
                    for dz in OFFSETS:
                        if dw == 0 and dx == 0 and dy == 0 and dz == 0:
                            continue
                        neighbor_coordinates = (w+dw, x+dx, y+dy, z+dz)
                        neighbor_is_active = neighbor_coordinates in active_grid
                        if neighbor_is_active:
                            active_neighbors += 1
                        else:
                            inactive_cells_to_check.add(neighbor_coordinates)

        if active_neighbors in (2,3):
            next_grid.add(key)

    #print(len(inactive_cells_to_check))
    for key in inactive_cells_to_check:
        w,x,y,z = key
        active_neighbors = 0
        for dw in OFFSETS:
            for dx in OFFSETS:
                for dy in OFFSETS:
                    for dz in OFFSETS:
                        neighbor_coordinates = (w+dw, x+dx, y+dy, z+dz)
                        neighbor_is_active = neighbor_coordinates in active_grid
                        if neighbor_is_active:
                            active_neighbors += 1

        if active_neighbors == 3:
            next_grid.add(key)

    return next_grid

def solve_part_2(puzzle_input):
    grid = set()

    for x in range(len(puzzle_input[0])):
        for y in range(len(puzzle_input)):
            if puzzle_input[y][x]:
                grid.add((0,x,y,0))

    for _ in range(6):
        #print(grid)
        grid = tick4d(grid)

    return len(grid)


def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(list(map(lambda c: c == "#", line)))

    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")