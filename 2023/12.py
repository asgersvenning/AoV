H = "#%"

class Groups:
    def __init__(self, groups : list[int]) -> None:
        self.elements = list(set(groups))
        self.counts = {length : 0 for length in self.elements}
        for group in groups:
            self.counts[group] += 1

    def without(self, index : int) -> "Groups":
        new_groups = [group for i, group in enumerate(self.elements) for _ in range(self.counts[group]) if i != index]
        return Groups(new_groups)
    
    def __len__(self) -> int:
        return len(self.elements)
    
    def __getitem__(self, index : int):
        elem = self.elements[index]
        return elem, self.counts[elem]
    
    def __iter__(self) -> "Groups":
        self._index = 0
        return self
    
    def __next__(self):
        if self._index < len(self):
            current = self[self._index]
            self._index += 1
            return current
        else:
            raise StopIteration
        
class Conditions:
    def __init__(self, conditions : str="") -> None:
        self.elements = [char for char in conditions]
        self.openings = []
        start, length = None, None
        for place, condition in enumerate(self.elements):
            if not condition == "#" and start is None:
                continue
            if condition == "#" and start is None:
                start = place
                length = 1
            elif condition == "#":
                length += 1
            else:
                if start is None or length is None:
                    raise RuntimeError("CONDITION")
                self.openings.append([start, length])
                start, length = None, None
        else:
            if start is not None:
                self.openings.append([start, length])

    def places(self, group : int) -> list[int]:
        places = []
        for start, length in self.openings:
            places += list(range(start, start + length - group + 1))
        return places
    
    def insert(self, group : int, place : int) -> "Conditions":
        if self[place - 1] in H or self[place+group] in H:
            return Conditions()
        new_elements = ["%" if i >= place and i < (place + group) else element for i, element in enumerate(self.elements)]
        if (place + group) < len(self):
            new_elements[place + group] = "."
        return Conditions("".join(new_elements))
    
    def __len__(self) -> int:
        return len(self.elements)
    
    def __getitem__(self, index : int):
        if index < 0 or index >= len(self):
            return "."
        try:
            return self.elements[index]
        except Exception as e:
            print(index, len(self))
            raise e
    
def parse_line(line) -> tuple["Conditions", "Groups"]:
        conditions, groups = line.strip().split(" ")

        return Conditions(conditions), Groups([int(i) for i in groups.split(",")])

def ways(conditions : "Conditions", groups : "Groups", first = True):
    print("".join(conditions.elements), ",".join([str(i) for i in groups.elements]))
    if len(conditions) == 0:
        return 0
    if len(groups) == 0:
        return 1
    w = 0
    group, _ = groups[0]
    places = conditions.places(group)
    # print("group:", group, "| conditions:", "".join(conditions.elements), "|", conditions.openings, "| places:", places)
    if len(places) == 0:
        return 0
    for place in places:
        w += ways(conditions.insert(group, place), groups.without(0), False)
    return w

path = "inputs/12.test1"

# with open(path, "r") as file:
#     ws = []
#     for i, line in enumerate(file.readlines()):
#         print("LINE:", i)
#         ws.append(ways(*parse_line(line)))
#     print(ws)

test_input = "#.#.#.#.# 1,1,1,1,1"
cond, grps = parse_line(test_input)

print(ways(cond, grps))