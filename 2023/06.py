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

from math import ceil, floor
import re

path = "inputs/06.test"

with open(path, "r") as f:
    time, distance = f.readlines()
    time = re.sub(r"\s+", " ", time.removeprefix("Time:").strip()).split(" ")
    distance = re.sub(r"\s+", " ", distance.removeprefix("Distance:").strip().replace("  ", " ")).split(" ")
    print(time)
    print(distance)
    time = [int(part) for part in time]
    distance = [int(part) for part in distance]

    races = [Race(t, d) for t, d in zip(time, distance)]

    total_ways = 1
    for race in races:
        roots = race.roots()
        if roots is None or (len(roots) == 1 and is_decimal(roots)) or (len(roots) == 2 and abs(roots[0] - roots[1]) < 1):
            total_ways = 0
            break
        if len(roots) == 2:
            assert roots[0] < roots[1], ValueError(f'Roots come in wrong order: {roots}')
            print(roots)
            total_ways *= floor(roots[1]) - ceil(roots[0])

    print(total_ways)
