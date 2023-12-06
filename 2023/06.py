class Race:
    def __init__(self, time, distance):
        self.time, self.distance = time, distance
        self.fun = lambda x : x * (self.time - x) - self.distance

    def roots(self):
        """
        Solution:\n
        `f(x) = x \\cdot (a - x) - b\n` 
        `-1 x^{2} + ax - b = 0\n`
        `x = \\frac{-b \\pm \\sqrt{b^2 - 4b}}{-2}`
        """ 
        a = -1
        b = self.time
        c = -self.distance

        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return None
        elif discriminant == 0:
            return -b / (2 * a)
        else:
            left, right = -b, discriminant ** (1/2)
            left, right = left / (2 * a), right / (2 * a)
            return left + right, left - right

def is_decimal(num):
    return num != (num // 1)

def ways(roots):
    if roots is None or (len(roots) == 1 and is_decimal(roots)) or (len(roots) == 2 and abs(roots[0] - roots[1]) < 1):
        return 0
    if len(roots) == 2:
        assert roots[0] < roots[1], ValueError(f'Roots come in wrong order: {roots}')
        w = floor(roots[1]) - ceil(roots[0]) + 1
        if not is_decimal(roots[0]) and not is_decimal(roots[1]):
            w -= 2
        return w
    else:
         return 1

from math import ceil, floor
import re

path = "inputs/06.input"

with open(path, "r") as f:
    # Part 1
    time, distance = f.readlines()
    time = re.sub(r"\s+", " ", time.removeprefix("Time:").strip()).split(" ")
    distance = re.sub(r"\s+", " ", distance.removeprefix("Distance:").strip().replace("  ", " ")).split(" ")
    time = [int(part) for part in time]
    distance = [int(part) for part in distance]

    races = [Race(t, d) for t, d in zip(time, distance)]

    total_ways = 1
    for race in races:
        roots = race.roots()
        this_ways = ways(roots)
        total_ways *= this_ways
    print(total_ways)

    # Part 2
    time = int("".join([str(part) for part in time]))
    distance = int("".join([str(part) for part in distance]))

    race = Race(time, distance)
    roots = race.roots()
    print(ways(roots))
