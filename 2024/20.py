import bisect

import numpy as np
from helpers import Animation, get_lines, get_path, STAR

from collections import Counter

from tqdm import tqdm

from copy import deepcopy

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

def directions(cheat_only : bool=False):
    # for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, 2), (2, 0), (0, -2), (-2, 0)]:
    for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)] if cheat_only else [(0, 1), (1, 0), (-1, 0), (0, -1), (0, 2), (2, 0), (0, -2), (-2, 0)]:
        yield (dx, dy)

class State:
    def __init__(self, i : int, j : int, total : int, last : "State | None"=None, cheats_left : int=1):
        self.i, self.j, self.total, self.last = i, j, total, last
        self.cheats_left = cheats_left
        self._hash = hash((i,j)) + (0 if self.last is None else self.last._hash)
        self.removed = []
        
    def move(self, direction : tuple[int, int]):
        cheating = sum(map(abs, direction)) == 2
        i, j, total = self.i + direction[0], self.j + direction[1], self.total + (2 if cheating else 1)
        return State(i, j, total, self, self.cheats_left - (1 if cheating else 0))
    
    def neighbors(self, mult : int=1, cheat_only : bool=False) -> "list[State] | filter[State]":
        if mult == 0:
            return [self]
        return filter(lambda x : x.cheats_left >= 0 and (self.last is None or x.ij != self.last.ij), (n for direction in directions(cheat_only) for n in self.move(direction).neighbors(mult - 1, cheat_only)))
    
    def iterbacktrace(self):
        this = self
        while this is not None:
            yield this
            this = this.last
    
    def backtrace(self) -> list["State"]:
        trace = []
        trace.append(self)
        while trace[-1].last is not None:
            trace.append(trace[-1].last)
        return trace
    
    @property
    def ij(self):
        return self.i, self.j
    
    def __hash__(self):
        return self._hash # hash(self.ij) ^ hash(self.last)
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __gt__(self, other : "State"):
        return (self.total >= other.total) or (self.cheats_left <= other.cheats_left)
    
    def __sub__(self, other):
        if self.total >= other.total:
            greater = self
            lesser = other
        else:
            greater = other
            lesser = self
        
        di, dj = greater.i - lesser.i, greater.j - lesser.j
        manh_dist = abs(di) + abs(dj)
        
        if abs(self.total - other.total) == manh_dist:
            path = []
            for p in greater.backtrace():
                path.append(p)
                if p == lesser:
                    break
            else:
                raise RuntimeError("UNEXPECTED END OF BACKTRACE")
            return path
        
        greater.cheats_left = 1000
        path = [greater]
        vi = 1 if di < 0 else -1
        while abs(di) > 0:
            sj = 0
            if abs(di) == 1:
                si = vi * 1
            else:
                si = vi * 2
            di += si
            path.append(path[-1].move((si, sj)))
                
        vj = 1 if dj < 0 else -1
        while abs(dj) > 0:
            si = 0
            if abs(dj) == 1:
                sj = vj * 1
            else:
                sj = vj * 2
            dj += sj
            path.append(path[-1].move((si, sj)))
        
        return list(reversed(path))
            
    
    @property
    def last_direction(self):
        if self.last is None:
            raise RuntimeError("Last direction not defined for initial state")
        lij = self.last.ij
        ij = self.ij
        return tuple(this - last for this, last in zip(ij, lij))
    
    @property
    def dstr(self):
        if self.last is None:
            return "S"
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
                return STAR
    
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

class PriorityQueue:
    def __init__(self, iterable=None):
        self.priority : list[int] = []
        self.items : list[State] = []
        self.seen : set = set()
        self._history : list[State] = []
        self.bans : set[State] = set()
        if not iterable is None:
            self += iterable

    def __len__(self):
        return len(self.items)
    
    def _minsert(self, iterable):
        [self._state_insert(item) if isinstance(item, State) else self._insert(*item) for item in sorted(iterable)]
        return self
        
    def _insert(self, priority : int, item):
        if item in self.bans:
            return self
        ins = bisect.bisect(self.priority, priority)
        self.priority.insert(ins, priority)
        self.items.insert(ins, item)
        return self
    
    def _state_insert(self, state : State):
        return self._insert(-state.total, state)
    
    def insert(self, *args):
        if len(args) == 1:
            return self._minsert(args[0])
        if len(args) == 2:
            return self._insert(*args)
        raise ValueError("???")
    
    def query_position(self, ij : tuple[int, int]):
        return [item for item in self.items if item.ij == ij]
    
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
    
    def remove(self, e : State):
        changed = False
        if e in self._history:
            changed = True
            self._history.remove(e)
            if e in self.seen:
                self.seen.remove(e)
        if e in self.items:
            changed = True
            i = self.items.index(e)
            self.items.pop(i)
            self.priority.pop(i)
        return changed
    
    def history(self):
        return self._history
    
def in_bounds(i : int, j : int, arr : np.ndarray):
    return 0 <= i < arr.shape[0] and 0 <= j < arr.shape[1]

def update(maze : np.ndarray, queue : PriorityQueue):
    _, nxt = queue.pop()
    if nxt is None or maze[*nxt.ij] == 0:
        return maze, queue
    valid_neighbors = [neighbor for neighbor in nxt.neighbors() if in_bounds(*neighbor.ij, maze) and maze[*neighbor.ij] != 0]
    queue += [neighbor for neighbor in valid_neighbors if all(other > neighbor for other in queue.query_position(neighbor.ij))]
    return maze, queue
     
def render_history(maze : np.ndarray, history : list[State], start : tuple[int, int], end : tuple[int, int]):
    blank_maze = np.zeros_like(maze)
    blank_maze[maze != 0] = 1
    blank_maze = [["." if v == 1 else "#" for v in row] for row in blank_maze]
    for i, state in enumerate(history):
        if state.ij == start:
            symbol = "S"
        elif state.ij == end:
            symbol = "E"
        else:
            symbol = history[i-1].dstr
        blank_maze[state.i][state.j] = f'[red bold]{symbol}[reset]'
    return "\n".join("".join(row) for row in blank_maze)

# def backtrace(history : list[State], target : tuple[int, int], start=-1):
#     # idx = start
#     # trace = [idx]
#     # while (current := history[trace[-1]]) != target:
#     #     trace.append([i for i, state in enumerate(history) if current.last == state and not i in trace][0])
#     # return [history[i] for i in trace]
#     init = history[start]
#     trace = [init]
#     while trace[-1].last is not None:
#         trace.append(trace[-1].last)
#     return trace
        

def shortest_path(type : str, start=None, end=None, maze=None, cheats : int=0):
    start, end, maze = (user if user is not None else parse for user, parse in zip([start, end, maze], parse_input(type)))

    queue = PriorityQueue([State(*start, 0, None, cheats)])
    
    while queue and maze[*end] == -1:
        update(maze, queue)

    return queue.history()[-1].backtrace()

def part1(type : str, threshold : int=100):
    normal_path = shortest_path(type)
    counts = {}
    
    for position in tqdm(normal_path[0].backtrace()):
        position.cheats_left = 1
        cheaters = [n for n in position.neighbors() if n.cheats_left == 0]
        savings = [meet[0].total - cheater.total for cheater in cheaters if (meet := [p for p in normal_path if p.ij == cheater.ij])]
        
        for saving in savings:
            if saving <= 0:
                continue
            if not saving in counts:
                counts[saving] = 0
            counts[saving] += 1
    
    return sum(v for k, v in counts.items() if k >= threshold)

# print(part1("test", 20))
print(part1("input", 100))

def manhattan(a, b):
    return abs(a.i - b.i) + abs(a.j - b.j)

def part2(type : str, threshold : int=100):
    normal_path = shortest_path(type)
    counts = {}
    
    def cost(*states):
        start, end = states[-1], states[0]
        return end.total - start.total
        
    trace = normal_path[0].backtrace()
    improvement = [cost(*trace[i:(i+j+1)]) - cost(*(first - last)) + 1 for i, last in enumerate(tqdm(trace)) for j, first in enumerate(trace[(i+1):]) if manhattan(first, last) <= 20]
    
    counts = Counter(improvement)
    
    return sum(v for k, v in counts.items() if k >= threshold)
    # return counts
    
# tp2 = part2("test", 50)
# for im in sorted(tp2, reverse=False):
#     if im <= 0:
#         continue
#     print(f'{im:>3} = {tp2[im]}')

# print(part2("test", 50))
# print(32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3)

print(part2("input", 100))



