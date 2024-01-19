import re
from interpreter import Interpreter


def parser(filename):
    with open(filename, "r") as file:
        file = file.read().splitlines()
    lst = []
    for i in file:
        lst += (re.split(r'\s+', i))

    new_list = list(filter(None, lst))
    interpreter = Interpreter()
    i = 0
    commands = []
    while i != len(new_list):
        if new_list[i] != "=":
            if new_list[i] == "SET":
                commands.append([new_list[i], new_list[i + 1], new_list[i + 3]])
                i += 4
            elif new_list[i] == "ENDIF" or new_list[i] == "ENDREPEAT" or new_list[i] == "ENDPROC":
                commands.append([new_list[i]])
                i += 1
            else:
                commands.append([new_list[i], new_list[i + 1]])
                i += 2
    interpreter = Interpreter()
    interpreter.load(commands)
    last = interpreter.next()
    coords = []
    while last is not None:
        coords.append(last)
        last = interpreter.next()
    return coords


if __name__ == '__main__':
    print(parser("test.txt"))
