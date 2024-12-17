import numpy as np

from helpers import Animation, get_lines, get_path

class Robot:
    def __init__(self, line : str, size : tuple[int, int]=(101, 103)):
        self.size = size
        self.position, self.velocity = [tuple(int(e) for e in p[2:].split(",")) for p in line.strip().split(" ")]
        if len(self.position) != 2 or len(self.velocity) != 2:
            raise RuntimeError(f"Unable to construct proper Robot(tm) from line: {line}, found {self.position = } and {self.velocity = }")
        
    def __call__(self, x : int):
        return tuple((a * x + b) % s for a, b, s in zip(self.velocity, self.position, self.size))
    
    def __str__(self):
        fmt = "p={},{} v={},{}"
        return fmt.format(*self.position, *self.velocity)
    
    def __repr__(self):
        return str(self)

def make_room(*robots : "Robot", it : int=0):
    size = set(robot.size for robot in robots)
    assert len(size) == 1
    size = size.pop()
    room = np.zeros(size, dtype=np.int64)
    for robot in robots:
        room[*robot(it)] += 1
    return room

def parse_input(type : str):
    size = (101, 103)
    if type == "test":
        size = (11, 7)
    return [Robot(line, size=size) for line in get_lines(get_path(type))]

def split_quadrants(room : np.ndarray):
    h, w = room.shape
    i_mid, j_mid = h // 2, w // 2
    left, right = room[:, :j_mid], room[:, (j_mid + 1):]
    left_top, left_bottom = left[:i_mid], left[(i_mid + 1):]
    right_top, right_bottom = right[:i_mid], right[(i_mid + 1):]
    return np.stack((left_top, right_top, right_bottom, left_bottom))

def room_cost(room : np.ndarray):
    return int(np.prod(split_quadrants(room).sum(-1).sum(-1)))

def part1(type : str):
    return room_cost(make_room(*parse_input(type), it=100))
    
# print(part1("test"))
print(part1("input"))

# Part 2

SYMBOLS = list("■●▲◆")
SQUARE, CIRCLE, TRIANGLE, DIAMOND = SYMBOLS

COLORS = ["green", "red", "yellow", "blue", "magenta", "cyan", "black", "white"]
    
def render(room : np.ndarray):
    return "\n".join(
        " ".join(
            # f"[bold {COLORS[v % (len(COLORS) - 2)]}]{v}[reset]" if v != 0 else " "
            SQUARE if v != 0 else " "
            for v in line
        )
        for line in room
    ) + "\n"

def part2(type : str):
    robots = parse_input(type)
    room_0_cost = room_cost(make_room(*robots))
    Animation(f"Iteration: {i}\n" + render(room) for i in range(10000) if room_cost(room := make_room(*robots, it=i)) < (room_0_cost / 4))(0, transient=False)

part2("input")