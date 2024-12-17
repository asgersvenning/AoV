from helpers import get_path, get_lines, Animation

def parse_input(type : str):
    map_lines, move_lines = [], []
    is_map = True
    for line in get_lines(get_path(type)):
        if line == "":
            is_map = False
            continue
        if is_map:
            map_lines.append(line)
        else:
            move_lines.append(line)
    return "\n".join(map_lines), "".join(move_lines)

class Object:
    def __init__(self, i : int, j : int, cls : str, map : "Map"):
        self.i = i
        self.j = j
        self.cls = cls
        self.map = map
    
    @property
    def ijs(self):
        return ((self.i,self.j),(self.i,self.j+1))

    def can_move(self, direction : str, n : int=1):
        if self.cls == "#":
            return False
        i, j = self.i, self.j
        match direction:
            case ">":
                j += n
            case "<":
                j -= n
            case "v":
                i += n
            case "^":
                i -= n
            case _:
                raise RuntimeError(f"Unknown direction {direction}")
        if self.cls != "[]":
            ij0 = (i, j - 1)
            ij = (i, j)
            if i < 0 or j < 0 or i >= self.map.height or j >= self.map.width or ij in self.map.walls:
                return False
            if ij == self.map.robot:
                raise RuntimeError("Attempted to move something into the robot??")
            if ij in self.map.boxes:
                return Object(*ij, "O", self.map).can_move(direction)
            if ij in self.map.large_boxes:
                return Object(*ij, "[]", self.map).can_move(direction)
            if ij0 in self.map.large_boxes:
                return Object(*ij0, "[]", self.map).can_move(direction)
            return True
        ijm1 = (i, j - 1)
        ij0 = (i, j)
        ij1 = (i, j + 1)
        if i < 0 or j < 0 or i >= self.map.height or (j + 1) >= self.map.width or ij0 in self.map.walls or ij1 in self.map.walls:
            return False
        if self.map.robot in [ij0, ij1]:
            raise RuntimeError("Attempted to move something into the robot??")
        new_boxes : list["Object"] = []
        new_large_boxes : list["Object"] = []
        if ij0 in self.map.boxes:
            new_boxes.append(Object(*ij0, "O", self.map))
        if ij1 in self.map.boxes:
            new_boxes.append(Object(*ij1, "O", self.map))
        if ijm1 in self.map.large_boxes and ijm1 != self:
            new_large_boxes.append(Object(*ijm1, "[]", self.map))
        if ij0 in self.map.large_boxes and ij0 != self:
            new_large_boxes.append(Object(*ij0, "[]", self.map))
        if ij1 in self.map.large_boxes and ij1 != self:
            new_large_boxes.append(Object(*ij1, "[]", self.map))
        return (all(box.can_move(direction) for box in new_boxes) and all(box.can_move(direction) for box in new_large_boxes))
    
    def move(self, direction : str, n : int=1):
        if self.cls == "#":
            return self
        i, j = self.i, self.j
        match direction:
            case ">":
                j += n
            case "<":
                j -= n
            case "v":
                i += n
            case "^":
                i -= n
            case _:
                raise RuntimeError(f"Unknown direction {direction}")
        if self.cls != "[]":
            ij0 = (i, j - 1)
            ij = (i, j)
            if i < 0 or j < 0 or i >= self.map.height or j >= self.map.width or ij in self.map.walls:
                return self
            if ij == self.map.robot:
                raise RuntimeError("Attempted to move something into the robot??")
            if ij in self.map.boxes:
                new_box = Object(*ij, "O", self.map)
                new_box.move(direction)
                if ij == new_box:
                    return self
                self.map.boxes.remove(ij)
                self.map.boxes.add(new_box)
            if ij in self.map.large_boxes:
                new_box = Object(*ij, "[]", self.map)
                new_box.move(direction)
                if ij == new_box:
                    return self
                self.map.large_boxes.remove(ij)
                self.map.large_boxes.add(new_box)
            if ij0 in self.map.large_boxes:
                new_box = Object(*ij0, "[]", self.map)
                new_box.move(direction)
                if ij0 == new_box:
                    return self
                self.map.large_boxes.remove(ij0)
                self.map.large_boxes.add(new_box)
            self.i, self.j = ij
            return self
        ijm1 = (i, j - 1)
        ij0 = (i, j)
        ij1 = (i, j + 1)
        if i < 0 or j < 0 or i >= self.map.height or (j + 1) >= self.map.width or ij0 in self.map.walls or ij1 in self.map.walls:
            return self
        if self.map.robot in [ij0, ij1]:
            raise RuntimeError("Attempted to move something into the robot??")
        new_boxes : list["Object"] = []
        new_large_boxes : list["Object"] = []
        if ij0 in self.map.boxes:
            new_boxes.append(Object(*ij0, "O", self.map))
        if ij1 in self.map.boxes:
            new_boxes.append(Object(*ij1, "O", self.map))
        if ijm1 in self.map.large_boxes and ijm1 != self:
            new_large_boxes.append(Object(*ijm1, "[]", self.map))
        if ij0 in self.map.large_boxes and ij0 != self:
            new_large_boxes.append(Object(*ij0, "[]", self.map))
        if ij1 in self.map.large_boxes and ij1 != self:
            new_large_boxes.append(Object(*ij1, "[]", self.map))
        if not (all(box.can_move(direction) for box in new_boxes) and all(box.can_move(direction) for box in new_large_boxes)):
            return self
        for lbox in new_large_boxes:
            self.map.large_boxes.remove(lbox)
            self.map.large_boxes.add(lbox.move(direction))
        for box in new_boxes:
            self.map.boxes.remove(box)
            self.map.boxes.add(box.move(direction))
        self.i, self.j = ij0
        return self
    
    @property
    def coordinate(self):
        return (self.i + 1) * 100 + self.j + 1 + (1 if self.cls == "[]" else 0)
    
    def __str__(self):
        match self.cls:
            case "@":
                pr = "robot"
            case "O":
                pr = "box"
            case "#":
                pr = "wall"
            case _:
                pr = "?"
        return f'{pr}: {self.i},{self.j}'
    
    def __repr__(self):
        return f'{type(self)}({str(self)})'
    
    def __hash__(self) -> int:
        return hash((self.i, self.j))
    
    def __eq__(self, other):
        return hash(self) == hash(other)

class Map:
    def __init__(self, init : str):
        rows = init.split("\n")
        self.width = len(rows[0]) - 2
        self.height = len(rows) - 2
        self.boxes : set["Object"] = set()
        self.large_boxes : set["Object"] = set()
        self.walls : set["Object"] = set()
        self.robot = None
        for _i in range(1, self.height + 1):
            i = _i - 1
            for _j in range(1, self.width + 1):
                j = _j - 1
                c = rows[_i][_j]
                match c:
                    case ".":
                        continue
                    case "O":
                        self.boxes.add(Object(i, j, c, self))
                    case "@":
                        self.robot = Object(i, j, c, self)
                    case "#":
                        self.walls.add(Object(i, j, c, self))
                    case _:
                        raise RuntimeError(f"Encountered unexpected tile at ({i}, {j}) in board:\n\n{init}")
        if self.robot is None:
            raise RuntimeError(f"Did not find any robot in board:\n\n{init}")
        self.robot : "Object"
    
    def move(self, direction : str):
        self.robot.move(direction)
        return self
    
    def enlarge(self):
        self.width *= 2
        self.robot = Object(self.robot.i, self.robot.j * 2, self.robot.cls, self)
        self.walls = set(Object(wall.i, wall.j * 2 + dj, "#", self) for wall in self.walls for dj in [0, 1])
        self.large_boxes = set(Object(box.i, box.j * 2, "[]", self) for box in self.boxes)
        self.boxes = set()
    
    def __str__(self):
        horiz_wall = "[black]" + "#" * (self.width + 2) + "[reset]"
        lines = [horiz_wall]
        for i in range(self.height):
            line = ["[black]#[reset]"]
            for j in range(self.width):
                ij = (i, j)
                if ij == self.robot:
                    c = "[bold red]@[reset]"
                elif ij in self.boxes:
                    c = "[white]O[reset]"
                elif ij in self.walls:
                    c = "[black]#[reset]"
                elif any(ij in lbox.ijs for lbox in self.large_boxes):
                    c = "[white]|[reset]"
                else:
                    c = "[black].[reset]"
                line.append(c)        
            line.append("[black]#[reset]")
            lines.append("".join(line))
        lines.append(horiz_wall)
        return "\n".join(lines)
    
    def __repr__(self):
        return f'{type(self)}:\n{str(self)}'

def animate(type : str, enlarge : bool=False, **kwargs):
    state, moves = parse_input(type)
    state = Map(state)
    if enlarge:
        state.enlarge()
    Animation(str(state.move(move)) for move in moves)(**kwargs)
    
def part1(type : str):
    state, moves = parse_input(type)
    state = Map(state)
    [state.move(move) for move in moves]
    return sum(box.coordinate for box in state.boxes)

def part2(type : str):
    state, moves = parse_input(type)
    state = Map(state)
    state.enlarge()
    [state.move(move) for move in moves]
    return sum(box.coordinate for box in state.boxes) + sum(box.coordinate for box in state.large_boxes)

# print(part1("test1"))
# print(part1("test"))
print(part1("input"))

# print(part2("test2"))
# print(part2("test"))
print(part2("input"))
