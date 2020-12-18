from rich import print

DIRECTIONS = ((1,0), (0,-1), (-1,0), (0,1))
DIRECTION_INDEX = {
    "E": DIRECTIONS[0],
    "S": DIRECTIONS[1],
    "W": DIRECTIONS[2],
    "N": DIRECTIONS[3]
}

def solve_part_1(puzzle_input):
    curX = 0
    curY = 0
    direction = 0
    for instruction, argument in puzzle_input:
        if instruction in DIRECTION_INDEX:
            dx, dy = DIRECTION_INDEX[instruction]
            curX += dx * argument
            curY += dy * argument

        elif instruction == "L":
            direction = (direction - argument // 90) % 4

        elif instruction == "R":
            direction = (direction + argument // 90) % 4

        elif instruction == "F":
            dx, dy = DIRECTIONS[direction]
            curX += dx * argument
            curY += dy * argument

    return abs(curX) + abs(curY)

def solve_part_2(puzzle_input):
    curX = 0
    curY = 0
    wayX = 10
    wayY = 1
    for instruction, argument in puzzle_input:
        if instruction in DIRECTION_INDEX:
            dx, dy = DIRECTION_INDEX[instruction]
            wayX += dx * argument
            wayY += dy * argument

        elif instruction == "L":
            for _ in range(argument // 90):
                temp = wayX
                wayX = -wayY
                wayY = temp

        elif instruction == "R":
            for _ in range(argument // 90):
                temp = wayX
                wayX = wayY
                wayY = -temp

        elif instruction == "F":
            curX += wayX * argument
            curY += wayY * argument

        #print((curX, curY), (wayX, wayY))
        #print()

    return abs(curX) + abs(curY)

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append( (line[0], int(line[1:])) )

    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")