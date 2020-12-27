import numpy as np
from rich import print

from collections import defaultdict
from functools import reduce

class Tile:
    def __init__(self, id):
        self.id = id
        self.bits = np.zeros((10,10), dtype=np.int8)


    def set_row(self, row, row_i):
        self.bits[row_i] = row


    def _bits_to_number(self, bits):
        x = 0
        for i, bit in enumerate(bits):
            x += (2 ** i) * bit

        return x


    def _get_edges(self, bits):
        return (self._bits_to_number(bits), self._bits_to_number(reversed(bits)))


    def get_edge_values(self):
        result = []
        result.extend(self._get_edges(self.bits[0]))
        result.extend(self._get_edges(self.bits[9]))
        result.extend(self._get_edges(self.bits[:,0]))
        result.extend(self._get_edges(self.bits[:,9]))
        
        return result

    def __repr__(self):
        return f"<Tile ({self.id})>"

def solve_part_1(puzzle_input):
    edge_compatability = defaultdict(set)
    for tile in puzzle_input:
        for edge in tile.get_edge_values():
            edge_compatability[edge].add(tile)

    #print(edge_compatability)
    #print(len(puzzle_input))
    counts = defaultdict(int)
    corner_candidates = defaultdict(int)
    for key in edge_compatability.keys():
        count = len(edge_compatability[key]) 
        counts[count] += 1
        if count == 1:
            for tile in edge_compatability[key]: # Should only be one, just familiar
                corner_candidates[tile] += 1

    #print(counts)
    #print(corner_candidates)

    result = 1
    for candidate, unique_edges in corner_candidates.items():
        if unique_edges == 4:
            result *= candidate.id

    return result

def solve_part_2(puzzle_input):
    return ""

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        cur_tile = None
        cur_row = 0
        for line in input_txt:
            if line.startswith("Tile"):
                cur_tile = Tile(int(line[4:9]))
                cur_row = 0
                puzzle_input.append(cur_tile)

            if line[0] in ("#","."):
                cur_tile.set_row([1 if c == "#" else 0 for c in line.strip()], cur_row)
                cur_row += 1
            
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")