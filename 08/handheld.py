from rich import print

def run(code):
    seen = set()
    cursor = 0
    acc = 0
    while cursor not in seen:
        if cursor == len(code):
            return acc, "finished"

        seen.add(cursor)
        
        instruction, amount = puzzle_input[cursor]

        if instruction == "nop":
            cursor += 1

        elif instruction == "jmp":
            cursor += amount

        elif instruction == "acc":
            acc += amount
            cursor += 1

    return acc, "looped"


def solve_part_1(puzzle_input):
    acc, state = run(puzzle_input)
    assert state == "looped"
    return acc


def solve_part_2(puzzle_input):
    for i in range(len(puzzle_input)):
        code_line = puzzle_input[i]
        if code_line[0] == "acc":
            continue

        elif code_line[0] == "nop":
            code_line[0] = "jmp"
            acc, state = run(puzzle_input)
            if state == "finished":
                return acc
            code_line[0] = "nop"

        elif code_line[0] == "jmp":
            code_line[0] = "nop"
            acc, state = run(puzzle_input)
            if state == "finished":
                return acc
            code_line[0] = "jmp"

    return "No code change found"

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            op, amount = line.split()
            puzzle_input.append([op, int(amount)])

    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")