from rich import print

from collections import defaultdict
from itertools import chain, combinations
import re

MEM_RE = re.compile("""
    ^
    mem
    \[([0-9]+)\]
    [ ]=[ ]
    ([0-9]+)
    $
""", re.X)

def powerset(iterable):
    # From the itertools documentation
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_masks(mask_string):
    passthrough = 0
    overwrite = 0
    for i, char in enumerate(reversed(mask_string)):
        if char == "X":
            passthrough |= 2 ** i

        else:
            overwrite |= int(char) * (2 ** i)

    return passthrough, overwrite


def solve_part_1(puzzle_input):
    passthrough_mask, overwrite_mask = (0,0)
    memory = defaultdict(int)
    for instruction in puzzle_input:
        if instruction[0] == "mask":
            passthrough_mask, overwrite_mask = get_masks(instruction[1])

        elif instruction[0] == "assign":
            address = instruction[1]
            initial_value = instruction[2]

            masked_value = initial_value & passthrough_mask | overwrite_mask
            memory[address] = masked_value

    return sum(memory.values())


def get_mem_decoder(mask_string):
    passthrough = 0
    overwrite = 0
    floating_bits = []
    for i, char in enumerate(reversed(mask_string)):
        if char == "0":
            passthrough |= 2 ** i

        elif char == "1":
            overwrite |= int(char) * (2 ** i)

        else:
            floating_bits.append(i)

    return passthrough, overwrite, floating_bits


def solve_part_2(puzzle_input):
    passthrough_mask, overwrite_mask, floating_bits = (0,0,[])
    memory = defaultdict(int)
    for instruction in puzzle_input:
        if instruction[0] == "mask":
            passthrough_mask, overwrite_mask, floating_bits = get_mem_decoder(instruction[1])

        elif instruction[0] == "assign":
            initial_address = instruction[1]
            value = instruction[2]

            base_address = initial_address & passthrough_mask | overwrite_mask
            for floating_bit_set in powerset(floating_bits):
                address = base_address
                for bit in floating_bit_set:
                    address += 2 ** bit

                memory[address] = value

    return sum(memory.values())


def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            if line.startswith("mask"):
                mask_string = line[7:7+36].strip()
                puzzle_input.append(("mask", mask_string))

            elif line.startswith("mem"):
                mem_match = MEM_RE.match(line)
                address = int(mem_match.group(1))
                value = int(mem_match.group(2))
                puzzle_input.append(("assign", address, value))

            else:
                raise Exception("No line match")

    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")