import re

from rich import print

LINE_RE = re.compile("""
    ^
    (.*)
    s[ ]contain[ ]
    (.*)
    [.]
    $
""", re.X)

CONTENT_RE = re.compile("""
    ([1-5])
    [ ]
    ([^,.]+?)
    s?[,.]
""", re.X)

bag_type_index = {}
class BagType:
    def __init__(self,name):
        self.name = name
        self.contents = []

    def contains(self, bag_type, amount):
        self.contents.append((bag_type, amount))

    def can_eventually_contain(self, target_bag):
        can_contain = False
        for bag_type, amount in self.contents:
            #print(f"Checking {bag_type}")
            if bag_type is target_bag:
                can_contain = True

            elif bag_type.can_eventually_contain(target_bag):
                can_contain = True

        return can_contain

    def count_decendants(self):
        total_decendants = 0
        for bag_type, amount in self.contents:
            total_decendants += amount
            total_decendants += amount * bag_type.count_decendants()
        
        return total_decendants

    def __repr__(self):
        return f"BagType({self.name})"

def solve_part_1(puzzle_input):
    count = 0
    target_bag = bag_type_index["shiny gold bag"]
    for bag_type in bag_type_index.values():
        #print(f"{bag_type}: ", end="")
        if bag_type.can_eventually_contain(target_bag):
            #print("True")
            count += 1
        #else:
            #print("False")

    return count

def solve_part_2(puzzle_input):
    target_bag = bag_type_index["shiny gold bag"]
    return target_bag.count_decendants()

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            match = LINE_RE.match(line)
            assert match is not None
            name = match.group(1)
            bag_type = BagType(name)
            bag_type_index[name] = bag_type

        input_txt.seek(0)

        for line in input_txt:
            #print(line)

            match = LINE_RE.match(line)
            assert match is not None
            name = match.group(1)
            bag_type = bag_type_index[name]
            #print(bag_type)

            for content_match in CONTENT_RE.finditer(line):
                #print(content_match.group(1))
                amount = int(content_match.group(1))
                child_type = bag_type_index[content_match.group(2)]
                #print(child_type, amount)
                bag_type.contains(child_type, amount)

    return bag_type_index

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(bag_type_index)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")