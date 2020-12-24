import re

from rich import print

RULE_RE = re.compile("""
    ^
    (?P<id>[0-9]+)
    :[ ]
    (?P<option1>[0-9 "ab]+)
    [|]?
    (?P<option2>[0-9 ]+)?
    $
""", re.X)


rule_index = {}
def parse_rule(line):
    line_match = RULE_RE.match(line)
    assert line_match is not None

    rule_id = int(line_match.group("id"))
    option1_string = line_match.group("option1")
    rule = None
    if '"' in option1_string:
        rule = SimpleRule(rule_id, ("a" if "a" in option1_string else "b"))
    else:
        option1 = list(map(int, option1_string.strip().split()))
        options = [option1]
        option2_string = line_match.group("option2")
        if option2_string is not None:
            option2 = list(map(int, option2_string.strip().split()))
            options.append(option2)

        rule = Rule(rule_id, options)

    rule_index[rule_id] = rule
    return rule_id, rule


class Rule:
    def __init__(self, id, options):
        self.id = id
        self._options = options

    def matches_all(self, message):
        matches, match_length = self.matches(message)
        return matches and match_length == len(message)

    def matches(self, message):
        greediest_option = 0
        for option in self._options:
            matches = True
            matched_up_to = 0
            for sub_rule_id in option:
                sub_rule = rule_index[sub_rule_id]
                substring = message[matched_up_to:]
                matches, submatch_up_to_index = sub_rule.matches(substring)
                if not matches:
                    break

                matched_up_to += submatch_up_to_index
            
            if matches:
                greediest_option = max(greediest_option, matched_up_to)

        if greediest_option > 0:
            return True, greediest_option

        #print(f"{message} fails rule {self.id}")
        return False, 0


class SimpleRule(Rule):
    def __init__(self, id, char):
        self.id = id
        self.character = char

    def matches(self, message):
        if message.startswith(self.character):

            #print(f"{message} matches rule {self.id}")
            return True, 1

        #print(f"{message} matches rule {self.id}")
        return False, 0


def solve_part_1(messages):
    rule_0 = rule_index[0]
    return sum((rule_0.matches_all(msg) for msg in messages))


def solve_part_2(messages):
    rule_42 = rule_index[42]
    rule_31 = rule_index[31]

    # Trying a number of rule 42 followed by a number of rule 31

    total = 0
    for message in messages:
        matches = False
        length_42 = 0
        matches_42 = []
        while length_42 < len(message) and matches is False:
            match_42, length_matched = rule_42.matches(message[length_42:])
            if not match_42:
                break
            length_42 += length_matched
            matches_42.append(length_matched)

            length_31 = 0
            matches_31 = []
            while length_42 + length_31 < len(message):
                match_31, length_matched = rule_31.matches(message[length_42 + length_31:])
                if not match_31:
                    break
                length_31 += length_matched
                matches_31.append(length_matched)

            if (
                length_42 + length_31 == len(message) 
                and length_31 > 0 
                and len(matches_42) >= len(matches_31) + 1
            ):
                matches = True
                break
    
        if matches:
            #print(message)
            total += 1

    return total


def get_puzzle_input():
    rules = []
    messages = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            if len(line.strip()) == 0:
                break
            rules.append(parse_rule(line))
        
        for line in input_txt:
            messages.append(line.strip())

    return rules, messages


if __name__ == "__main__":
    rules, messages = get_puzzle_input()

    answer_1 = solve_part_1(messages)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(messages)
    print(f"Part 2: {answer_2}")