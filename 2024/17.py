from helpers import get_lines, get_path, Animation

class Computer:
    def __init__(self, instructions : list[int], A : int, B : int, C : int, debug : bool=False):
        self.instructions = instructions
        self.A, self.B, self.C = A, B, C
        self.pointer = 0
        self.output = []
        self.log = []
        self.debug = debug
        
    def __str__(self):
        instructions = ",".join(map(str, self.instructions))
        empty = [" "] * 2 * max(len(self), self.pointer * 2)
        pointer = empty
        pointer[self.pointer * 2] = "🠉"
        pointer = "".join(pointer)
        registers = f"A = {self.A}\nB = {self.B}\nC = {self.C}"
        return "\n".join([instructions, pointer, "", registers])
    
    def __repr__(self):
        return f"{type(self)}[{len(self)}]:\n{self}"
    
    def __len__(self):
        return len(self.instructions)
        
    def __call__(self):
        if self.pointer >= len(self):
            raise IndexError("OUT-OF-BOUNDS ACCESS")
        opcode, operand = self.OP(self.instructions[self.pointer]), self.instructions[self.pointer+1]
        if self.debug:
            self.log.append(f"{opcode} {operand}")
        getattr(self, opcode)(operand)
        self.pointer += 2
    
    def OP(self, key : int):
        fn = None
        match key:
            case 0:
                fn = "adv"
            case 1:
                fn = "bxl"
            case 2:
                fn = "bst"
            case 3:
                fn = "jnz"
            case 4:
                fn = "bxc"
            case 5:
                fn = "out"
            case 6:
                fn = "bdv"
            case 7:
                fn = "cdv"
            case _:
                raise RuntimeError(f"UNKNOWN OPCODE: {key}")
        return fn
    
    def combo(self, x : int):
        if x <= 3:
            return x
        match x:
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                raise NotImplementedError("OPERAND 7 IS RESERVED")
            case _:
                raise RuntimeError(f"UNKNOWN OPERAND: {x}")
    
    def adv(self, x : int):
        self.A = int(self.A / (2 ** self.combo(x)))
    
    def bxl(self, x : int):
         self.B = self.B ^ x
         
    def bst(self, x : int):
        self.B = self.combo(x) % 8
         
    def jnz(self, x : int):
        if self.A != 0:
            self.pointer = x - 2
        
    def bxc(self, x : int):
        self.B = self.B ^ self.C
        
    def out(self, x : int):
        self.output.append(self.combo(x) % 8)
        
    def bdv(self, x : int):
        self.B = int(self.A / (2 ** self.combo(x)))
    
    def cdv(self, x : int):
        self.C = int(self.A / (2 ** self.combo(x)))
        
def parse_input(type : str):
    A, B, C, program = [line.split(": ")[-1] for line in get_lines(get_path(type)) if line]
    return Computer([int(n) for n in program.split(",")], int(A), int(B), int(C))

def part1(type : str, animate : bool=False):
    anim = Animation()
    computer = parse_input(type)

    while True:
        if animate:
            anim += str(computer)
        try:
            computer()
        except IndexError:
            break
    if animate:
        anim(0.1)
    return ",".join(map(str, computer.output))

print(part1("test1"))

def flips(outputs : list[str]):
    if len(outputs) == 0:
        raise ValueError()
    N = len(outputs[0])
    deltas = {i : [] for i in range(N)}
    last = {i : 0 for i in range(N)}
    for i, (this, nxt) in enumerate(zip(outputs, outputs[1:])):
        for j in range(N):
            if this[j] != nxt[j]:
                delta = i - last[j]
                deltas[j].append(delta)
                last[j] = i + 1
    return {k : list(set(v)) for k, v in deltas.items()}

def part2(type : str, verbose : bool=True):
    def inner(computer : Computer):
        while True:
            try:
                computer()
            except IndexError:
                return computer.output
    
    original = parse_input(type)
    outputs = []
    upper = (2 ** 3) ** (len(original))
    i = lower = (2 ** 3) ** (len(original) - 1)
    j = 0
    for K in reversed(range(len(original))):
        this_delta = int(2 ** (3 * (K - 1)))
        for i in range(lower, upper, max(1, this_delta)):
            output = inner(Computer(original.instructions, i, original.B, original.C))
            if output[K:] == original.instructions[K:]:
                outputs.append(output)
                lower = i
                break
            if verbose and j % 1000 == 0:
                print(f"\r{i}", end="")
            j += 1
    if verbose:
        print("\r", end="")
    return i

print(part2("input"))