import re

class Card:
    def __init__(self, s : str):
        s = s.strip().replace("  ", " ")
        card, numbers = s.split(": ")
        self.winning, self.found = [[int(i) for i in n.split(" ")] for n in numbers.split(" | ")]
        self.number = int(card.removeprefix("Card "))
        self.copies = 1

    def count(self):
        return sum([i in self.winning for i in self.found])

    def score(self):
        n = self.count()
        if n == 0:
            return 0
        else:
            return 2 ** (n - 1)

    def __str__(self):
        return f'Card {self.number}x{self.copies}: {" ".join([str(i) for i in self.winning])} | {" ".join([str(i) for i in self.found])}'        


path = "inputs/04.input"
with open(path, "r") as f:
    cards = [Card(line) for line in f.readlines()]
    scores = [card.score() for card in cards]
    print(sum(scores))

    wins_array = [card.count() for card in cards]
    for i, wins in enumerate(wins_array):
        n_copies = min(len(cards) - i, wins)
        if wins == 0:
            continue
        for card in cards[(i + 1):(i + n_copies + 1)]:
            card.copies += cards[i].copies

    print(sum([card.copies for card in cards]))


