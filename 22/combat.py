from rich import print

from collections import deque

def get_puzzle_input():
    decks = {
        "Player 1": deque(),
        "Player 2": deque()
    }

    building_deck = None
    with open("input.txt") as input_txt:
        for line in input_txt:
            if line.startswith("P"):
                building_deck = decks[line[:8]]

            else:
                try:
                    card = int(line)
                    building_deck.append(card)
                except:
                    pass

    return (decks["Player 1"], decks["Player 2"])

def score(deck:deque):
    score = 0
    for i, card in enumerate(reversed(deck)):
        score += (i+1) * card
    return score

def solve_part_1(player1:deque, player2:deque):
    while len(player1) > 0 and len(player2) > 0:
        player1_card = player1.popleft()
        player2_card = player2.popleft()

        # No ties in this game
        worse_card, better_card = sorted((player1_card, player2_card))

        victor = player1 if better_card == player1_card else player2
        victor.append(better_card)
        victor.append(worse_card)

    winner = player1 if len(player1) > 0 else player2
    return score(winner)

def recursive_combat(player1:deque, player2:deque, score=False):
    # Player 1 and Player 2 are not to be reassigned. We want to return the
    # winner in the exact object we were given.

    hands_seen = set()
    while len(player1) > 0 and len(player2) > 0:
        hashable_hand = (tuple(player1), tuple(player2))
        if hashable_hand in hands_seen:
            #print("Player1 wins by default")
            return player1
        hands_seen.add(hashable_hand)

        player1_card = player1.popleft()
        player2_card = player2.popleft()

        victor = None
        if player1_card <= len(player1) and player2_card <= len(player2):
            # Some backflips here to get a slice
            sub_player1 = deque(tuple(player1)[:player1_card])
            sub_player2 = deque(tuple(player2)[:player2_card])
            assert len(sub_player1) > 0 and len(sub_player2) > 0
            sub_winner = recursive_combat(sub_player1, sub_player2)
            victor = player1 if sub_winner is sub_player1 else player2

        else:
            # No ties in this game
            victor = player1 if player1_card > player2_card else player2

        victor.append(player1_card if victor is player1 else player2_card)
        victor.append(player2_card if victor is player1 else player1_card)

    winner = player1 if len(player1) > 0 else player2
    return winner

def solve_part_2(player1, player2):
    winner = recursive_combat(player1, player2)
    return score(winner)

if __name__ == "__main__":
    player1, player2 = get_puzzle_input()

    answer_1 = solve_part_1(deque(player1), deque(player2))
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(deque(player1), deque(player2))
    print(f"Part 2: {answer_2}")