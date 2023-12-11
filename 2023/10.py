from colorama import Fore, Style
from typing import Union
from copy import deepcopy

SYMBOL_TO_DIRECTION = {
    "|" : ["UP", "DOWN"],
    "-" : ["LEFT", "RIGHT"],
    "L" : ["UP", "RIGHT"],
    "J" : ["UP", "LEFT"],
    "7" : ["DOWN", "LEFT"],
    "F" : ["DOWN", "RIGHT"],
    "." : [],
    "S" : ["START"]
}
DIRECTION_TO_OFFSET = {
    "RIGHT" : [0, 1],
    "UP" : [1, -1],
    "LEFT" : [0, -1],
    "DOWN" : [1, 1]
}
REFLECT = {
    "UP" : "DOWN",
    "DOWN" : "UP",
    "LEFT" : "RIGHT",
    "RIGHT" : "LEFT"
}

class Pipe:
    def __init__(self, symbol : str, position: list[int]) -> None:
        self.symbol = symbol
        self.directions = SYMBOL_TO_DIRECTION[self.symbol]
        if self.symbol == "S":
            self.start = True
            self.directions = []
        else:
            self.start = False
        self.position = position
    
    def go(self, direction : str) -> list[int, int]:
        new_position, offset = list(self.position), DIRECTION_TO_OFFSET[direction]
        new_position[offset[0]] += offset[1]
        return new_position
    
    def go_to_chain(self, chain : "Chain", direction : "str") -> int:
        global board, counted
        n = 0
        x,y = self.go(direction)
        on_chain = chain.check_pos(x,y)
        while (not on_chain) and x >= 0 and y >= 0 and x < board.width and y < board.height:
            on_chain = chain.check_pos(x,y)
            if counted[y][x] == 0 and not on_chain:
                n += 1
            if not on_chain:
                counted[y][x] += 1
            w, o = DIRECTION_TO_OFFSET[direction]
            if w == 0:
                x += o
            else:
                y += o
        return n
    
    def connections(self) -> Union[None, tuple[list, list]]:
        if self.directions is None:
            return None
        return self.directions, [self.go(direction) for direction in self.directions]
        
    def query_connection(self, tboard : list[list]) -> list:
        neighbors = {direction : self.go(direction) for direction in DIRECTION_TO_OFFSET}
        cons = []
        for di, (xi, yi) in neighbors.items():
            neighbor = tboard[[xi, yi]]
            _, ncon = neighbor.connections()
            for xj, yj in ncon:
                if xj == self.position[0] and yj == self.position[1]:
                    cons.append(di)
        return cons

    def __str__(self) -> str:
        return (Fore.LIGHTBLACK_EX if self.symbol == "." else (Fore.GREEN if self.symbol == "S" else Fore.CYAN)) + ("■" if self.symbol == "." else self.symbol) + Fore.RESET
    
class Chain:
    def __init__(self, start : "Pipe") -> None:
        self.open = True
        self.pipes = [start]
        self.hash_check = {"000" : None}
        self.hash_check.update({self.create_hash(start) : None})

    def __getitem__(self, index : int) -> "Pipe":
        return self.pipes[index]
    
    def __iter__(self) -> "Chain":
        mtul = [sum(i.position) for i in self.pipes]
        upper_left = [i for i, (d, p) in enumerate(zip(mtul, self.pipes)) if d == min(mtul) and "RIGHT" in p.directions and self.check(p)].pop()
        left, middle, right = self.pipes[:upper_left], [self.pipes[upper_left]], self.pipes[(upper_left + 1):]
        self.pipes = list(middle + right + left)
        check_direction = self.pipes[0].go("RIGHT") == self.pipes[1].position
        if not check_direction:
            self.pipes = [self.pipes[0]] + self.pipes[::-1]
        self._index, self._last_dir, self._normal = 0, "RIGHT", "DOWN"
        return self
    
    def __next__(self) -> "Pipe":
        if self._index < (len(self) - 1):
            current = self[self._index]
            directions = current.directions
            if self._index == 0:
                new_direction = "RIGHT"
            else:
                new_direction = [i for i in directions if i != REFLECT[self._last_dir]].pop()
            ray_count = current.go_to_chain(self, self._normal)
            if new_direction == self._last_dir:
                pass
            else:
                if new_direction == self._normal:
                    self._normal, ray_count = REFLECT[self._last_dir], 0
                else:
                    self._normal = self._last_dir 
                    ray_count += current.go_to_chain(self, self._normal)
                self._last_dir = new_direction
            self._index += 1
            return ray_count
        raise StopIteration

    def create_hash(self, pipe : "Pipe") -> str:
        return '{},{}'.format(*pipe.position)

    def check(self, other : "Pipe") -> bool:
        return self.create_hash(other) in self.hash_check
    
    def check_pos(self, x : int, y : int) -> bool:
        return f'{x},{y}' in self.hash_check

    def insert(self, new : "Pipe", index : int) -> None:
        if self.check(new):
            self.open = False
        else:
            index = len(self) - index + 1 if index < 0 else index                
            self.hash_check.update({self.create_hash(new) : None})
            self.pipes.insert(index, new)

    def __len__(self) -> int:
        return len(self.pipes)
    
    def where(self, x, y) -> int:
        for i, pipe in enumerate(self.pipes):
            xi, yi = pipe.position
            if xi == x and yi == y:
                return i
        else:
            return -1
    
    def distance(self, x : int, y : int) -> list[int]:
        position = self.where(x, y)
        return [min(abs(position - i), abs(position - (len(self) + i))) for i in range(len(self))]
    
    def _propagate(self, current : Union[None, "Pipe"]=None, prior : Union[list, list[str]]=[]):
        global board
        current = self.pipes[0] if current is None else current            
        old_directions = deepcopy(current.directions)
        [current.directions.remove(REFLECT[p]) for p in prior if REFLECT[p] in current.directions]   
        dcon, con = current.connections()
        fd = [d for d in DIRECTION_TO_OFFSET if d in dcon].pop(0) if len(con) == 2 else dcon[0]
        dcon, con = fd, con[dcon.index(fd)]
        current.directions = old_directions
        new = deepcopy(board[con])
        self.insert(new, -1)
        return new, [dcon]

    def follow(self) -> "Chain":
        _next = self._propagate()
        while self.open:
            _next = self._propagate(*_next)
         
class Board:
    def __init__(self, rows : list[list["Pipe"]]) -> None:
        self.rows, self.width, self.height = rows, len(rows[0]), len(rows)

    def __len__(self) -> int:
        return sum([len(row) for row in self.rows])

    def __getitem__(self, i : Union[int, list[int, int]]) -> "Pipe":
        x, y = (i % self.width, i // self.width) if isinstance(i, int) else i
        return self.rows[y][x]


path = "inputs/10.input"

with open(path, "r") as file:
    board = Board([[Pipe(c, [x, y]) for x, c in enumerate(line.strip())] for y, line in enumerate(file.readlines())])

    # Part 1 - Follow the loop
    start = None
    for pipe in board:
        if pipe.start:
            start = pipe
            break
    
    start.directions = start.query_connection(board)
    chain = Chain(deepcopy(start))
    chain.follow()
    print(max(chain.distance(*start.position)))

    # Part 2 - Shoot inside the chain
    counted = [[0] * board.width for _ in range(board.height)]
    print(sum([ray for ray in chain]))


### EXTRA CODE FOR TERMINAL VIZ
    # # Creates initial map
    # for row in board.rows:
    #     for elem in row:
    #         print(elem, end = "")
    #     print()
    # # Creates map for part 2
    # for row, (rowc, rowp) in enumerate(zip(counted, board.rows)):
    #     for col, (count, elem) in enumerate(zip(rowc, rowp)):
    #         if count != 0:
    #             print(Style.BRIGHT + Fore.BLUE + str(count) + Fore.RESET + Style.RESET_ALL, end = " ")
    #         # else:
    #         #     print(count, end ="")
    #         else:
    #             if chain.check_pos(col, row):
    #                 print(Style.BRIGHT + Fore.RED + elem.symbol + Fore.RESET + Style.RESET_ALL, end = " ")
    #             else:
    #                 print(elem, end = " ")
    #     print()