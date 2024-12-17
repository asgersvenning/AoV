import numpy as np
from tqdm import tqdm

from helpers import Animation, get_lines, get_path

def parse_input(type : str):
    lines = get_lines(get_path(type))
    arr = -np.ones((len(lines), len(lines[0])))
    start, end = (0, 0), (0, 0) 
    for i, line in enumerate(lines):
        for j, e in enumerate(line):
            match e:
                case "S":
                    start = (i, j)
                case "E":
                    end = (i, j)
                case "#":
                    arr[i,j] = 0
    return start, end, arr

def directions():
    for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        yield (dx, dy)

class State:
    def __init__(self, i : int, j : int, total : int, last_direction : tuple[int, int]):
        self.i, self.j, self.total, self.last_direction = i, j, total, last_direction
        
    def move(self, direction : tuple[int, int]):
        i, j, total = self.i + direction[0], self.j + direction[1], self.total + 1
        if direction != self.last_direction:
            total += 1000
        return State(i, j, total, direction)
    
    def neighbours(self):
        return (self.move(direction) for direction in directions())
    
    @property
    def ij(self):
        return self.i, self.j
    
    def __hash__(self):
        return hash(self.ij)
    
    def __eq__(self, other : "State"):
        return hash(self) == hash(other)
    
    def __lt__(self, other : "State"):
        return self.total < other.total
    
    @property
    def dstr(self):
        match self.last_direction:
            case (0, 1):
                return ">"
            case (0, -1):
                return "<"
            case (1, 0):
                return "v"
            case (-1, 0):
                return "^"
            case _:
                raise RuntimeError()
    
    def __str__(self):
        return f'{self.dstr} : ({self.i}, {self.j})'
    
    def __repr__(self):
        return str(self)

def argmin(iterable):
    mv, mi = float("inf"), None
    for i, v in enumerate(iterable):
        if v < mv:
            mv, mi = v, i
    return mi

def order(iterable):
    return [i for i, _ in sorted(enumerate(iterable), key=lambda x : x[1])]

import bisect


class PriorityQueue:
    def __init__(self, iterable=None):
        self.priority : list[int] = []
        self.items : list[State] = []
        self.seen : set = set()
        self._history : list[State] = []
        if not iterable is None:
            self += iterable

    def __len__(self):
        return len(self.items)
    
    def _minsert(self, iterable):
        [self._state_insert(item) if isinstance(item, State) else self._insert(*item) for item in sorted(iterable)]
        return self
        
    def _insert(self, priority : int, item):
        ins = bisect.bisect(self.priority, priority)
        self.priority.insert(ins, priority)
        self.items.insert(ins, item)
        return self
    
    def _state_insert(self, state : State):
        return self._insert(-state.total, state)
    
    def insert(self, *args):
        if len(args) == 1:
            return self._minsert(args[0])
        elif len(args) == 2:
            return self._insert(*args)
        else:
            raise ValueError("???")
    
    def __radd__(self, other):
        return self.insert(other)
    
    def __iadd__(self, other):
        return self.insert(other)
    
    def pop(self):
        if len(self) == 0:
            return None, None
        p, e = self.priority.pop(), self.items.pop()
        if e in self.seen:
            return self.pop()
        self.seen.add(e)
        self._history.append(e)
        return p, e
    
    def history(self):
        return self._history

def update(maze : np.ndarray, queue : PriorityQueue):
    _, nxt = queue.pop()
    if nxt is None:
        return maze, queue
    cost = nxt.total
    maze[*nxt.ij] = cost
    queue += [neighbor for neighbor in nxt.neighbours() if maze[*neighbor.ij] != 0 and maze[*neighbor.ij] <= cost]
    return maze, queue
     
def render_history(maze : np.ndarray, history : list[State], start : tuple[int, int], end : tuple[int, int]):
    blank_maze = np.zeros_like(maze)
    blank_maze[maze != 0] = 1
    blank_maze = [["." if v == 1 else "#" for v in row] for row in blank_maze]
    for i, state in enumerate(history):
        if state == start:
            symbol = "S"
        elif state == end:
            symbol = "E"
        else:
            symbol = history[i-1].dstr
        blank_maze[state.i][state.j] = f'[red bold]{symbol}[reset]'
    return "\n".join("".join(row) for row in blank_maze)

def backtrace(history : list[State], target : tuple[int, int], start=-1):
    idx = start
    trace = [idx]
    while (last := history[trace[-1]]) != target:
        ij = tuple(p - d for p, d in zip(last.ij, last.last_direction))
        trace.append([i for i, state in enumerate(history) if ij == state and not i in trace][0])
    return [history[i] for i in trace]

def part1(type : str, animate : bool=False, verbose : bool=False):
    start, end, maze = parse_input(type)

    queue = PriorityQueue([State(*start, 0, (0, 1))])
    
    anim = Animation()
    while queue and maze[*end] == -1:
        update(maze, queue)
        if animate:
            anim += render_history(maze, queue.history(), start, end)

    best_path = backtrace(queue.history(), start)
    if verbose or animate:
        last_frame = render_history(maze, best_path, start, end)
        width = len(last_frame.split("\n", maxsplit=1)[0])
        last_frame += f'\n{f'Total = {best_path[0].total}':^{width}}'
        if animate:
            anim += last_frame
            anim(0.01)
        elif verbose:
            Animation([last_frame])(0)
    return best_path[0].total

# part1("test", True)
# part1("test1", True)
print(part1("input"))

def all_best_paths(history : list[State], start : tuple[int, int], verbose : bool=False):
    paths = [backtrace(history, start)]
    visited = set(map(lambda x : x.ij, paths[0]))
    iterable_history = reversed(history)
    if verbose:
        iterable_history = tqdm(iterable_history, total=len(history))
    for _i, state in enumerate(iterable_history):
        i = len(history) - _i - 1
        if state.ij in visited:
            continue
        for neighbor in state.neighbours():
            new_path = None
            if neighbor in visited:
                for path in paths:
                    if neighbor in path:
                        break
                match_idx = path.index(neighbor)
                match = path[match_idx]
                if match.total == neighbor.total or (abs(match.total - neighbor.total) == 1000 and match.last_direction != path[match_idx - 1].last_direction):
                    new_path = [e for e in backtrace(history, start, i) if not e in visited]
            if new_path is not None:
                paths.append(new_path)
                [visited.add(e.ij) for e in new_path]
    return paths

def part2(type : str, animate : bool=False, verbose : bool=False):
    start, end, maze = parse_input(type)

    queue = PriorityQueue([State(*start, 0, (0, 1))])
    
    anim = Animation()
    while queue and maze[*end] == -1:
        update(maze, queue)
        if animate:
            anim += render_history(maze, queue.history(), start, end)
    
    best_paths = all_best_paths(queue.history(), start, verbose)
    all_states = [state for path in best_paths for state in path]
    visited_tiles = set(map(lambda x : x.ij, all_states))
    if verbose or animate:
        last_frame = render_history(maze, all_states, start, end)
        width = len(last_frame.split("\n", maxsplit=1)[0])
        last_frame += f'\n{f'Total = {len(visited_tiles)}':^{width}}'
        if animate:
            anim += last_frame
            anim(0.01)
        elif verbose:
            Animation([last_frame])(0)
    
    return len(visited_tiles)

# part2("test", True)
# part2("test1", True)
print(part2("input"))