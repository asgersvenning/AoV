class Space:
    def __init__(self, lines : list[str], expansion : int=2) -> None:
        self.lines = [line.strip() for line in lines]
        expansion -= 1
        lines = [[c for c in line] for line in self.lines]
        rowsums, colsums = [0] * len(lines), [0] * len(lines[0])
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == ".":
                    continue
                rowsums[row], colsums[col] = rowsums[row] + 1, colsums[col] + 1
        self.rows, self.cols = [0] * len(lines), [0] * len(lines[0])
        row_acc = 0
        for row, rowsum in enumerate(rowsums):
            if rowsum == 0:
                row_acc += 1
            self.rows[row] = row + row_acc * expansion
        col_acc = 0
        for col, colsum in enumerate(colsums):
            if colsum == 0:
                col_acc += 1
            self.cols[col] = col + col_acc * expansion
        self.galaxies = [Galaxy(x, y) for y, line in zip(self.rows, self.lines) for x, symbol in zip(self.cols, line) if symbol == "#"]
    
class Galaxy:
    def __init__(self, x : int, y : int):
        self.x, self.y = x, y

    def __sub__(self, other : "Galaxy") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)
    
path = "inputs/11.input"

with open(path, "r") as file:
    file_lines = file.readlines()
    # Part 1
    space = Space(file_lines)
    print(sum([gi - gj for j, gj in enumerate(space.galaxies) for i, gi in enumerate(space.galaxies) if i < j]))
    
    # Part 2
    space = Space(file_lines, 1000000)
    print(sum([gi - gj for j, gj in enumerate(space.galaxies) for i, gi in enumerate(space.galaxies) if i < j]))
