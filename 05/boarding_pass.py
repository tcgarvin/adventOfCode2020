from rich import print

def get_row_column(spec):
    row_spec = spec[:7]
    col_spec = spec[7:]

    row_spec = row_spec.replace("F", "0").replace("B", "1")
    row = int(row_spec,2)

    col_spec = col_spec.replace("L", "0").replace("R", "1")
    col = int(col_spec,2)

    return row, col

def solve_part_1(puzzle_input):
    highest_id = 0
    for line in puzzle_input:
        row,col = get_row_column(line)
        seat_id = row * 8 + col
        highest_id = max(highest_id, seat_id)

    return highest_id

def solve_part_2(puzzle_input):
    all_seats = [False] * 1024
    for line in puzzle_input:
        row,col = get_row_column(line)
        seat_id = row * 8 + col
        all_seats[seat_id] = True

    for i in range(1,1023):
        if all_seats[i] is False and all_seats[i-1] is True and all_seats[i+1] is True:
            return i

    return "Not found"

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(line)
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")