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
    "UP" : [1, -1],
    "RIGHT" : [0, 1],
    "DOWN" : [1, 1],
    "LEFT" : [0, -1]
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

    @property
    def x(self) -> int:
        return self.position[0]
    
    @property
    def y(self) -> int:
        return self.position[1]
    
    def go(self, direction : str) -> list[int, int]:
        new_position = list(self.position)
        offset = DIRECTION_TO_OFFSET[direction]
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
                if xj == self.x and yj == self.y:
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
        print("Start running on chain")
        mtul = [sum(i.position) for i in self.pipes]
        upper_left = [i for i, (d, p) in enumerate(zip(mtul, self.pipes)) if d == min(mtul) and "RIGHT" in p.directions and self.check(p)].pop()
        left, middle, right = self.pipes[:upper_left], [self.pipes[upper_left]], self.pipes[(upper_left + 1):]
        self.pipes = list(middle + right + left)
        #### CHECK DIRECTION OF LOOP - May not be needed
        check_direction = self.pipes[0].go("RIGHT") == self.pipes[1].position
        if not check_direction:
            self.pipes = [self.pipes[0]] + self.pipes[::-1]
        # print("START POSITION:", self.pipes[0].position, self.pipes[0].symbol, self.pipes[0].directions)
        #####
        self._index = 0
        self._last_dir = "RIGHT"
        self._normal = "DOWN"
        return self
    
    def __next__(self) -> "Pipe":
        if self._index < (len(self) - 1): # Assume that the last pipe doesn't need 
            ## When going to the next pipe in the chain, the new normal can be found using the following cases:
            # 1) If the next pipe is not going to turn, the normal stays the same
            # 2) If the next pipe is going to turn:
            # 2.1) If the next pipe is turning in the direction of the normal, set the new normal to the opposite of the old direction
            # 2.2) If the next pipe is turning in the opposite direction of the normal, set the new normal to the old direction
            # OBS: during the turn query both the old and new normal from the corner pipe
            current = self[self._index]
            #inner = current.go_to_chain(self, self._normal)
            directions = current.directions
            if self._index == 0:
                new_direction = "RIGHT"
            else:
                new_direction = [i for i in directions if i != REFLECT[self._last_dir]].pop()
            # print(current, new_direction, self._normal)
            if new_direction == self._last_dir:
                ray_count = current.go_to_chain(self, self._normal)
            elif new_direction == REFLECT[self._last_dir]:
                raise RuntimeError(f'Unexpected direction {new_direction} coming from {current.position} ({self._last_dir})')
            else:
                if new_direction == self._normal:
                    self._normal = REFLECT[self._last_dir]
                    ray_count = 0
                else:
                    ray_count = current.go_to_chain(self, self._normal)
                    self._normal = self._last_dir
                    ray_count += current.go_to_chain(self, self._normal)
                self._last_dir = new_direction
            self._index += 1
            return ray_count
        print("Finished running on chain")
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
            if index < 0:
                index = len(self) - index + 1
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
    
    def _propagate(self, current : Union[None, "Pipe"]=None, prior : Union[None, list[str]]=None, direction : Union[list[int], list[int, int]]=[0, -1]):
        global board
        if current is None:
            current = self.pipes[0]
        old_directions = deepcopy(current.directions)
        if not prior is None:
            for p in prior:
                pr = REFLECT[p]
                if pr in current.directions:
                    current.directions.remove(pr)
        dcons, cons = current.connections()
        current.directions = old_directions
        bfs_queue = []
        for dir, dcon, con in zip(direction, dcons, cons):
            xc, yc = con
            # Skip out of bounds connections
            if xc < 0 or yc < 0 or xc >= board.width or yc >= board.height:
                continue
            new = deepcopy(board[[xc, yc]])
            self.insert(new, dir)
            if self.open is False:
                break
            bfs_queue.append([new, [dcon], [dir]])
        return bfs_queue

    def bfs(self) -> "Chain":
        _next = self._propagate()
        while self.open:
            _next = [elem for i in _next for elem in self._propagate(*i)]
         
class Board:
    def __init__(self, rows : list[list["Pipe"]]) -> None:
        self.rows = rows
        self.width = len(self.rows[0])
        self.height = len(self.rows)

    def __len__(self) -> int:
        return sum([len(row) for row in self.rows])

    def __getitem__(self, i : Union[int, list[int, int]]) -> "Pipe":
        if isinstance(i, int):
            assert i < len(self), IndexError(f"Index '{i}' out of bounds for board of size {len(self)}")
            x, y = i % self.width, i // self.width
        elif isinstance(i, list):
            x, y = i
        else:
            raise TypeError(f"Unsupported indexing type of '{type(i)}' to Board")
        assert x < self.width and y < self.height, IndexError(f"Indexes (x,y)='{x},{y}' out of bounds for board of size ({self.width},{self.height})")
        return self.rows[y][x]

    def __iter__(self) -> "Board":
        self._current_index = 0
        return self
    
    def __next__(self) -> "Pipe":
        if self._current_index < len(self):
            x = self[self._current_index]
            self._current_index += 1
            return x
        raise StopIteration


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
    chain.bfs()
    distances = chain.distance(*start.position)
    print(max(distances))
    print()

    for row in board.rows:
        for elem in row:
            print(elem, end = " ")
        print()

    # Part 2 - Shoot inside the chain
    counted = []
    for row in range(board.height):
        counted.append([])
        for elem in range(board.width):
            counted[-1].append(0)
    area = 0
    for ray in chain:
        # print(ray)
        area += ray
    print()
    for row, (rowc, rowp) in enumerate(zip(counted, board.rows)):
        for col, (count, elem) in enumerate(zip(rowc, rowp)):
            if count != 0:
                print(Style.BRIGHT + Fore.BLUE + str(count) + Fore.RESET + Style.RESET_ALL, end = " ")
            # else:
            #     print(count, end ="")
            else:
                if chain.check_pos(col, row):
                    print(Style.BRIGHT + Fore.RED + elem.symbol + Fore.RESET + Style.RESET_ALL, end = " ")
                else:
                    print(elem, end = " ")
        print()
    print()
    print(area)
    