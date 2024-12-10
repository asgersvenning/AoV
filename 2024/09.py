import bisect
import time

from sortedcontainers import SortedDict
from helpers import *

def parse_input(type : str):
    return list(map(int, get_lines(get_path(type))[0]))

def expand_view(data : list[int], ids : list[bool]) -> list[str]:
    return [c for size, id in zip(data, ids) for c in [str(id) if id != -1 else "."] * size]

def spans(indices, size):
    return SortedDict({indices[start + 1] : indices[start + 1] + end - start for start, end in zip(([-1] + breaks), (breaks + [size]))} if (breaks := [p for p, (i, j) in enumerate(zip(indices, indices[1:])) if (j - i) > 1]) else {})

class File:
    def __init__(self, id, disk, start=None, size=None, indices=None, maintain_disk : bool=True, with_spans : bool=False):
        self._maintain_disk, self._with_spans = maintain_disk, with_spans
        self.disk, self.file, self.id = disk, id != -1, (id if id != -1 else None)
        self.indices = list(range(start, start+size))if indices is None else sorted(indices)
        self.spans = spans(self.indices, len(self)) if self._with_spans else None

    def __len__(self):
        return len(self.indices)

    def __iadd__(self, i : int):
        bisect.insort(self.indices, i)
        if self._maintain_disk:
            self.disk[i] = str(self.id) if self.file else "."
        if self._with_spans:
            self.spans : SortedDict
            for j, (start, end) in enumerate(self.spans.items()):
                if ((overshoot := i - (end - 1)) == 1) | ((undershoot := start - i) == 1) | (overshoot > 1):
                    break
            else:
                self.spans[i] = i + 1
                return self

            if overshoot == 1 or undershoot == 1:
                if overshoot == 1:
                    next_start, next_end = self.spans.peekitem(j + 1)
                    if (next_start - end) <= 2:
                        self.spans.pop(next_start)
                    self.spans[start] = next_end if (next_start - end) <= 2 else self.spans[start] + 1
                if undershoot == 1:
                    prev_start, prev_end = self.spans.peekitem(j - 1)
                    self.spans.pop(start)
                    self.spans[(prev_start if (start - prev_end) <= 2 else (start - 1))] = end
        return self

    def __isub__(self, i : int):
        self.indices.pop(bisect.bisect(self.indices, i) - 1)
        if self._maintain_disk:
            self.disk[i] = "?"
        if self._with_spans:
            self.spans : SortedDict
            for start, end in self.spans.items():
                if start <= i < end:
                    break
            else:
                raise RuntimeError(f"Attempted to remove index ({i}) but couldn't find a matching span")

            if (end - start) <= 1:
                self.spans.pop(start)
            else:
                if i == start:
                    self.spans[start + 1] = self.spans.pop(start)
                elif i == end:
                    self.spans[start] -= 1
                else:
                    self.spans[start], self.spans[i+1] = i, end
        return self

    def swap(self, other : "File", i : int, j : int):
        if i in self.indices and j in other.indices:
            self -= i
            other -= j
            self += j
            other += i
        else:
            raise RuntimeError(f"Swap index ({i}) must be present in left or right object")

    def checksum(self):
        assert self.file, TypeError("Cannot compute checksum for space-type file", self)
        return sum(i * int(self.id) for i in self.indices)

    def __repr__(self):
        name = f"FILE[{self.id}]" if self.file else "SPACE"
        return f"{name} | [{','.join(map(str, self.indices))}]"

def preprocess(data : list[int], visualize : slice | bool | None=False):
    disk, vis = expand_view(data, [int(i // 2) if i % 2 == 0 else -1 for i in range(len(data))]), None

    if isinstance(visualize, bool):
        visualize = None if not visualize else slice(0, len(disk), 1)
    if not visualize is None:
        print(vis := "|".join(disk[visualize]), end="")

    files, space = {}, []
    [space.append(i) if e == "." else files.update({e : files.get(e, []) + [i]}) for i, e in enumerate(disk)]

    return disk, files, space, visualize, vis

def part1(data : list[int], visualize : slice | bool | None=False):

    disk, files, space, visualize, vis = preprocess(data, visualize)

    files = {str(id) : File(id, disk, indices=i) for id, i in files.items()}
    space, j = File(-1, disk, indices=space), len(disk) - 1

    for i in range(j):
        if disk[i] == ".":
            while not disk[j].isdigit():
                j -= 1

            if i >= j:
                break
            space.swap(files[disk[j]], i, j)
            if not visualize is None:
                if vis != (next_vis := "\r" + "|".join(disk[visualize])):
                    time.sleep(0.2)
                    print(vis := next_vis, end="")
    if not visualize is None:
        print()

    return sum(file.checksum() for _, file in files.items())

# print(part1(parse_input("test"), True))
print(part1(parse_input("input")))

def part2(data : list[int], visualize : slice | bool | None=False):

    disk, files, space, visualize, vis = preprocess(data, visualize)

    files = SortedDict({int(id) : File(id, disk, indices=i, maintain_disk=not visualize is None) for id, i in files.items()})
    space = File(-1, disk, indices=space, maintain_disk=not visualize is None, with_spans=True)

    for id in reversed(files):
        file = files[id]
        for start in space.spans:
            if start > file.indices[0]:
                break
            if (space.spans[start] - start) >= len(file):
                [space.swap(file, i, j) for i, j in zip(range(start, start + len(file)), file.indices.copy())]

        if not visualize is None:
            if vis != (next_vis := "\r" + "|".join(disk[visualize])):
                time.sleep(0.2)
                print(vis := next_vis, end="")
    if not visualize is None:
        print()

    return sum(file.checksum() for _, file in files.items())

# print(part2(parse_input("test"), True))
print(part2(parse_input("input")))
