import numpy as np
from rich import print

from collections import defaultdict
from functools import reduce


#1:                  # 
#2:#    ##    ##    ###
#3: #  #  #  #  #  #   
SEA_MONSTER = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1],
    [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0]
])
SEA_MONSTER_SUM = np.sum(SEA_MONSTER)

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

    def left(self):
        return self._bits_to_number(self.bits[:,0])

    def top(self):
        return self._bits_to_number(self.bits[0])

    def right(self):
        return self._bits_to_number(self.bits[:,9])

    def bottom(self):
        return self._bits_to_number(self.bits[9])

    def _get_edges(self, bits):
        return (self._bits_to_number(bits), self._bits_to_number(reversed(bits)))


    def get_edge_values(self):
        result = []
        result.extend(self._get_edges(self.bits[0]))
        result.extend(self._get_edges(self.bits[9]))
        result.extend(self._get_edges(self.bits[:,0]))
        result.extend(self._get_edges(self.bits[:,9]))
        
        return result

    def rotate(self):
        self.bits = np.rot90(self.bits)

    def orient(self, edge_value, direction):
        method = getattr(self, direction)
        
        for i in range(4):
            self.rotate()
            if method() == edge_value:
                return

        self.bits = np.fliplr(self.bits)

        for i in range(4):
            self.rotate()
            if method() == edge_value:
                return

        raise Exception(f"Could not match {self}, {direction}, {edge_value}")

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
    any_corner = None
    for candidate, unique_edges in corner_candidates.items():
        if unique_edges == 4:
            result *= candidate.id
            any_corner = candidate

    return result, edge_compatability, any_corner

def solve_part_2(puzzle_input, edge_compatability, any_corner):
    # First, get the 2D array of all tiles, each oriented properly
    unplaced_tiles = set(puzzle_input)

    # Previous solving revealed the shape is 12x12 tiles
    
    tile_grid = []
    for i in range(12):
        tile_grid.append([None] * 12)

    for i in range(12):
        for j in range(12):
            if i == 0 and j == 0:
                correct_tile = any_corner
                rotation_found = False
                while rotation_found == False:
                    correct_tile.rotate()
                    left_side = correct_tile.left()
                    top_side = correct_tile.top()

                    if len(edge_compatability[left_side]) == 1 and len(edge_compatability[top_side]) == 1:
                        rotation_found = True

            else:
                if j == 0:
                    di = -1
                    dj = 0
                    adjacent_tile = tile_grid[i-1][j]
                else:
                    di = 0
                    dj = -1
                    adjacent_tile = tile_grid[i][j-1]

                if adjacent_tile is None:
                    print(tile_grid, i, j)
                    raise Exception("Could not find adjacent tile")

                edge_to_match = adjacent_tile.right()
                if di == -1:
                    edge_to_match = adjacent_tile.bottom()

                correct_tile = None
                for tile in edge_compatability[edge_to_match]:
                    if tile == adjacent_tile:
                        continue
                    correct_tile = tile

                correct_tile.orient(edge_to_match, "left" if di == 0 else "top")
            
            tile_grid[i][j] = correct_tile
            unplaced_tiles.remove(correct_tile)

    #print(tile_grid)

    # Generate the actual grid

    grid = np.zeros((12*8,12*8), dtype=np.int8)

    for i in range(12):
        for j in range(12):
            gridi = i * 8
            gridj = j * 8
            grid[gridi:gridi+8, gridj:gridj+8] = tile_grid[i][j].bits[1:9, 1:9]

    sea_monsters = np.zeros((12*8,12*8), dtype=np.int8)
    
    for i in range(4):
        grid = np.rot90(grid)
        sea_monsters = np.rot90(sea_monsters)
        detect_sea_monster(grid, sea_monsters)

    grid = np.fliplr(grid)
    sea_monsters = np.fliplr(sea_monsters)

    for i in range(4):
        grid = np.rot90(grid)
        sea_monsters = np.rot90(sea_monsters)
        detect_sea_monster(grid, sea_monsters)

    for row in grid:
        print("".join("#" if x == 1 else "." for x in row))

    print()

    for row in sea_monsters:
        print("".join("#" if x == 1 else "." for x in row))



    return np.sum(grid) - np.sum(sea_monsters)

def detect_sea_monster(grid, sea_monsters):
    for i in range(12 * 8 - 2):
        for j in range(12 * 8 - 19):
            mask_sum = np.sum(np.bitwise_and(SEA_MONSTER, grid[i:i+3, j:j+20]))
            if mask_sum == SEA_MONSTER_SUM:
                #print("found one")
                sea_monsters[i:i+3, j:j+20] = SEA_MONSTER

            elif mask_sum > 9:
                #print(grid[i:i+3, j:j+20])
                #print(mask_sum)

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

    answer_1, edge_compatability, any_corner = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input, edge_compatability, any_corner)
    print(f"Part 2: {answer_2}")