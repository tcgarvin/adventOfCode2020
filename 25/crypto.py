from rich import print
from rich.progress import track

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(int(line))
    return puzzle_input

def crack_loop_size(result):
    subject_number = 7
    value = 1
    loop_number = 0
    while value != result:
        value = (value * subject_number) % 20201227
        loop_number += 1

    return loop_number

def generate_key(opposing_public_key, loop_number):
    subject_number = opposing_public_key
    value = 1
    for i in track(range(loop_number)):
        value = (value * subject_number) % 20201227

    return value

def solve_part_1(puzzle_input):
    card_public_key, door_public_key = puzzle_input
    card_loop_size = crack_loop_size(card_public_key)
    print(f"Card Loop Size: {card_loop_size}")
    door_loop_size = crack_loop_size(door_public_key)
    print(f"Door Loop Size: {door_loop_size}")

    encryption_key_a = generate_key(card_public_key, door_loop_size)
    print(f"Door-generated Key: {encryption_key_a}")
    encryption_key_b = generate_key(door_public_key, card_loop_size)
    print(f"Card-generated Key: {encryption_key_b}")

    return encryption_key_a

def solve_part_2(puzzle_input):
    return ""

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")