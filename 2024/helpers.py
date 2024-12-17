import os
from inspect import stack
from time import sleep
from typing import Iterator

from rich.console import Console
from rich.live import Live


def get_path(type : str="test"):
    dir, file = os.path.split(stack()[1].filename)
    return os.path.join(dir, "inputs", os.path.splitext(file)[0] + "." + type)

def get_lines(path : str):
    with open(path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def get_input_matrix(path : str, cls : type=int):
    return [list(map(cls, line)) for line in get_lines(path)]

def animate_frames(frames, speed=0.05, **kwargs):
    console = Console()  # Create a Console object
    with Live("", console=console, refresh_per_second=1/speed, **kwargs) as live:
        for frame in frames:
            live.update(frame)  # Update the displayed frame
            sleep(speed)
    
class Animation:
    def __init__(self, frames : list[str] | Iterator[str] | None=None):
        self.frames = list(frames or [])
    
    def __add__(self, other : str):
        self.frames.append(other)
        return self
    
    def __radd__(self, other : str):
        return self + other
        
    def __iadd__(self, other : str):
        return self + other
    
    def __len__(self):
        return len(self.frames)
    
    def __getitem__(self, i):
        return self.frames[i]
    
    def __call__(self, speed : float=0.05, transient : bool=True, **kwargs):
        if len(self) > 0:
            animate_frames(self.frames, speed, transient=transient, **kwargs)
