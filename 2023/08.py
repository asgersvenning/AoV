import re
from typing import Union
from math import prod

class Node:
    def __init__(self, line : str):
        line = line.strip()
        line = re.sub(r"[\=\(\),]", "", line)
        line = re.sub(r"\s+", " ", line)
        self.name, self.left, self.right = line.split(" ")
    
    def __str__(self) -> str:
        return f'{self.name} = ({self.left}, {self.right})'

class Network:
    def __init__(self, lines : list[str]):
        self.lines = lines
        self.network = {}
        self._parse()

    def _parse(self) -> None:
        self.nodes = [Node(line) for line in self.lines]
        self.nodes = {node.name : node for node in self.nodes}
        for node in self.nodes:
            if node[-1] == "A":
                self.position = node
                break
    
    def __str__(self) -> str:
        return "\n".join([str(node) for _, node in self.nodes.items()])
    
    def move(self, direction : str) -> str:
        if direction == "R":
            self.position = self.nodes[self.position].right
        elif direction == "L":
            self.position = self.nodes[self.position].left
        else:
            raise ValueError(f"Expected 'direction' to be a string of either 'R' of 'L'!")
        return self.position
    
    def copy(self, start : Union[str, None]=None):
        new_network = Network(self.lines)
        if not start is None:
            new_network.position = start
        return new_network
    
def steps(ntw : "Network"):
    global directions
    steps = 0
    while ntw.position[-1] != "Z":
        current_direction = directions[steps % len(directions)]
        ntw.move(current_direction)
        steps += 1
    return steps

def prime_factorize(n : int) -> list[int]:
    primes = []
    if n % 2 == 0:
        primes.append(2)
        n /= 2
    while n > 1:
        for i in range(3, n, 2):
            if n % i == 0:
                primes.append(i)
                n /= i
    return primes
    
path = "inputs/08.input"

with open(path, "r") as file:
    # Part 1 - Follow direction
    input_lines = file.readlines()
    directions = input_lines[0].strip()
    network = Network(input_lines[2:])

    print(steps(network))

    # Part 2 - Be a ghost!
    networks = [network.copy(start) for start in [node for node in network.nodes if node[-1] == "A"]]
    del network
    
    all_steps = [steps(network) for network in networks]

    step_primes = []
    for ts in all_steps:
        step_primes += prime_factorize(ts)
    step_primes = list(set(step_primes))

    print(prod(step_primes))