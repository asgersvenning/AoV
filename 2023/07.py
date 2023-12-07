STRENGTH = {label : i for i, label in enumerate(reversed("A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")))}
TYPES = list(reversed(["FIVE", "FOUR", "HOUSE", "THREE", "TWO", "ONE", "HIGHEST"]))

class Type:
    def __init__(self, cards : list[str], jokers : bool):
        self.counts = [0] * len(STRENGTH)
        for card in cards:
            if jokers and card == "J":
                continue
            self.counts[STRENGTH[card]] += 1
        self.max = max(self.counts)
        if jokers:
            highest = None
            for i, count in enumerate(self.counts):
                if count == self.max:
                    highest = i
                    break
            self.counts[highest] += sum([card == "J" for card in cards])
            self.max = self.counts[highest]   
        if self.max > 3:
            self.strength = self.max + 1
        elif self.max == 3 and 2 in self.counts:
            self.strength = 4
        elif self.max == 3:
            self.strength = 3
        elif self.max == 2 and sum([count == 2 for count in self.counts]) == 2:
            self.strength = 2
        elif self.max == 2:
            self.strength = 1
        else:
            self.strength = 0

    def __gt__(self, other : "Type") -> bool:
        return self.strength > other.strength

    def __lt__(self, other : "Type") -> bool:
        return self.strength < other.strength

    def __str__(self) -> str:
        return TYPES[self.strength]

class Hand:
    def __init__(self, s : str, jokers : bool = False):
        self.hand, self.bid = s.strip().split(" ")
        self.cards = list(self.hand)
        self.bid = int(self.bid)
        self.type = Type(self.cards, jokers)
        self._jokers = jokers

    @property
    def jokers(self) -> bool:
        return self._jokers

    @jokers.setter
    def jokers(self, value : bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"'jokers' attribute must be a boolean, found {type(value)}")
        self.type = Type(self.cards, value)
        self._jokers = value

    def compare(self, other : "Hand"):
        if self.type > other.type:
            return 1
        if self.type < other.type:
            return -1
        card_equal = True
        for i in range(5):
            scard, ocard = STRENGTH[self.cards[i]], STRENGTH[other.cards[i]]
            if self.jokers:
                if scard == STRENGTH["J"]:
                    scard = -1
                if ocard == STRENGTH["J"]:
                    ocard = -1
            card_equal = scard == ocard
            comparison = scard > ocard
            if not card_equal:
                break
        else:
            return 0
        
        if comparison:
            return 1
        else:
            return -1
        
    def __str__(self) -> str:
        return f'Cards: {" ".join(self.hand)} | Bid = {self.bid:>5}'
        
def sort_hands(hand_list : list["Hand"]) -> list["Hand"]:
    if not isinstance(hand_list, list):
        raise TypeError(f"Expected type list but 'hands' is {type(hand_list)}")
    if len(hand_list) == 0:
        raise TypeError(f"Expected non-empty list but hands has length {len(hand_list)}")
    if len(hand_list) == 1:
        return hand_list
    elif len(hand_list) == 2:
        compare = hand_list[0].compare(hand_list[1])
        if compare == 0:
            return hand_list
        elif compare == 1:
            return hand_list
        elif compare == -1:
            return hand_list[::-1]
        else:
            raise RuntimeError(f"Invalid compare value {compare}!")
    else:
        mid_point = len(hand_list) // 2
        left, right = sort_hands(hand_list[:mid_point]), sort_hands(hand_list[mid_point:])
        new_list = []
        for _ in range(len(left) + len(right)):
            compare = left[0].compare(right[0])
            if compare == -1:
                new_list.append(right.pop(0))
            else:
                new_list.append(left.pop(0))
            if not left or not right:
                break
        return new_list + left + right
    
def winnings(hand_list : list["Hand"]) -> int:
    sorted_hands = sort_hands(hand_list)
    winnings = 0
    for rank, hand in enumerate(reversed(sorted_hands)):
        winnings += (rank + 1) * hand.bid
    return winnings

path = "inputs/07.input"

with open(path, "r") as file:
    # Part 1
    hands = [Hand(line) for line in file.readlines()]
    print("Part 1:", winnings(hands))

    # Part 2 - Jokers
    for i in range(len(hands)):
        hands[i].jokers = True

    sorted_hands = sort_hands(hands)
    print("Part 2:", winnings(hands))
