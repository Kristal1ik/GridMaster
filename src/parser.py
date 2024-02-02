import re
from src.interpreter import Interpreter


def parser(filename):
    delete_com = ["", "="]
    with open(filename, "r") as file:
        file = list(filter(lambda item: item != "", file.read().splitlines()))
    commands = []
    for row in file:
        commands.append(list(filter(lambda com: com not in delete_com, (re.split(r'\s+', row)))))
    interpreter = Interpreter()
    interpreter.load(commands)
    last = interpreter.next()
    coords = []
    while last is not None:
        coords.append(last)
        try:
            last = interpreter.next()
        except Exception as e:
            return e, coords

    return None, coords


if __name__ == '__main__':
    print(parser("test.txt"))