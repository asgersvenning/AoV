def parse_input(lines : list[str]) -> list[int]:
    return [[int(part) for part in line.strip().split(" ")] for line in lines]

class Sequence:
    def __init__(self, numbers : list[int]):
        self.numbers = numbers

    def __eq__(self, x : int) -> list[bool]:
        return [i == x for i in self.numbers]
    
    def __len__(self) -> int:
        return len(self.numbers)
    
    def max_len(self) -> int:
        return max([len(str(num)) for num in self.numbers])
    
    def __str__(self, max_len : int) -> str:
        ss = [str(num) for num in self.numbers]
        ss = [s + " " * max(0, max_len - len(s) + 2) for s in ss]
        return "".join(ss)
    
    def __getitem__(self, i):
        return self.numbers[i]
    
    def append(self, x : int) -> None:
        self.numbers.append(x)

    def prepend(self, x : int) -> None:
        self.numbers.insert(0, x)
    
    def diff(self) -> "Sequence":
        return Sequence([self.numbers[i+1] - self.numbers[i] for i in range(len(self) - 1)])

class History:
    def __init__(self, sequence : list[int]):
        self.sequence = Sequence(sequence)
        self.history : list["Sequence"] = []
        self.forward()
        self.backward()

    def forward(self):
        self.last_sequence = self.sequence
        while not all(self.last_sequence == 0):
            self.history.append(self.last_sequence)
            self.last_sequence = self.last_sequence.diff()
        self.history.append(self.last_sequence)

    def backward(self):
        self.history[-1].append(0)
        self.history[-1].prepend(0)
        for i in range(1, len(self.history)):
            i = len(self.history) - i - 1
            # Forward interpolation
            self.history[i].append(self.history[i][-1] + self.history[i + 1][-1])
            # Backward interpolation
            self.history[i].prepend(self.history[i][0] - self.history[i + 1][0])

    def future(self):
        return self.history[0][-1]
    
    def past(self):
        return self.history[0][0]

    def __str__(self) -> str:
        ss = [sequence.__str__(max_len = self.sequence.max_len()) for sequence in self.history]
        max_len = max([len(s) for s in ss])
        return "\n".join([f'{s:^{max_len}}' for s in ss])
    

path = "inputs/09.input"

with open(path, "r") as file:
    histories = [History(pline) for pline in parse_input(file.readlines())]

    # Part 1 - To the future
    print(sum([history.future() for history in histories]))
    # Part 2 - Back to the past
    print(sum([history.past() for history in histories]))