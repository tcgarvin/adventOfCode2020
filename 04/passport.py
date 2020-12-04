import re

REQUIRED = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
COLOR_RE = re.compile("^[#][0-9a-f]{6}$")
EYE_COLORS = set(["amb","blu","brn","gry","grn","hzl","oth"])
PID_RE = re.compile("^[0-9]{9}$")

def solve_part_1(puzzle_input):
    num_valid = 0
    for record in puzzle_input:
        print(record.keys())
        if set(record.keys()).issuperset(REQUIRED):
            num_valid += 1
            print("OK")

    return num_valid

def solve_part_2(puzzle_input):
    num_valid = 0
    for record in puzzle_input:
        print(record)
        if not set(record.keys()).issuperset(REQUIRED):
            continue

        byr = record["byr"]
        if len(byr) != 4 or int(byr) < 1920 or int(byr) > 2002:
            print("bad byr")
            continue

        iyr = record["iyr"]
        if len(iyr) != 4 or int(iyr) < 2010 or int(iyr) > 2020:
            print("bad iyr")
            continue

        eyr = record["eyr"]
        if len(eyr) != 4 or int(eyr) < 2020 or int(eyr) > 2030:
            print("bad eyr")
            continue

        hgt, hgt_unit = record["hgt"][:-2], record["hgt"][-2:]
        if hgt_unit not in ("cm", "in"):
            print("bad hgt_unit")
            continue

        hgt = int(hgt)
        if hgt_unit == "cm" and (hgt < 150 or hgt > 193):
            print("bad hgt")
            continue

        if hgt_unit == "in" and (hgt < 59 or hgt > 76):
            print("bad hgt")
            continue

        if COLOR_RE.match(record["hcl"]) is None:
            print("bad hcl")
            continue

        if record["ecl"] not in EYE_COLORS:
            print("bad ecl")
            continue

        if PID_RE.match(record["pid"]) is None:
            print("bad pid")
            continue

        num_valid += 1
        print("OK")


    return num_valid

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        record = {}
        puzzle_input.append(record)
        for line in input_txt:
            if len(line.strip()) == 0:
                record = {}
                puzzle_input.append(record)
                continue

            fields = line.split()
            for field in fields:
                key, value = field.split(":")
                record[key] = value

    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")