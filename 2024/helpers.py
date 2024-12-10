import os
from inspect import stack


def get_path(type : str="test"):
    dir, file = os.path.split(stack()[1].filename)
    return os.path.join(dir, "inputs", os.path.splitext(file)[0] + "." + type)

def get_lines(path : str):
    with open(path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]