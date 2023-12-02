import timeit

input_path = "input_01.txt"

with open(input_path, "r") as f:
    values = [[int(i) for i in l.split("\n")] for l in f.read().strip().split("\n\n")]

# Part 1
def part_1():
    Answer_1 = max([sum(v) for v in values])
    return Answer_1

# Part 2
def part_2():
    sums = [sum(v) for v in values]

    class top_3:
        def __init__(self):
            self.top = [0, 0, 0]
        
        def __add__(self, other):
            if other > self.top[0]:
                self.top[0] = other
                self.top.sort()
            return self
            
        def __repr__(self):
            return str(self.top)
        
        def sum(self):
            return sum(self.top)

    Answer_2 = top_3()

    for s in sums:
        Answer_2 = Answer_2 + s
        
    return Answer_2.sum()

# Results
print("Results:")
print("Part 1:", part_1())
print("Part 2:", part_2())
        
# Time the two parts
print("Time:")
print("Part 1:", timeit.timeit(part_1, number=10000))
print("Part 2:", timeit.timeit(part_2, number=10000))

