class Function:
    def __init__(self, name, code):
        self.code = code
        self.name = name


class Actions:
    @staticmethod
    def move(interpreter, direction, distance):
        match direction:
            case "RIGHT":
                interpreter.x += distance
            case "LEFT":
                interpreter.x -= distance
            case "UP":
                interpreter.y += distance
            case "DOWN":
                interpreter.y -= distance
            case _:
                raise Exception(f"Неизвестное направление {direction}")

    @staticmethod
    def checkIf(interpreter, direction):
        match direction:
            case "RIGHT":
                if interpreter.x != 10:
                    return False
            case "LEFT":
                if interpreter.x != -10:
                    return False
            case "UP":
                if interpreter.y != 10:
                    return False
            case "DOWN":
                if interpreter.y != -10:
                    return False
            case _:
                raise Exception(f"Неизвестное направление {direction}")
        return True

    @staticmethod
    def call(interpreter, funcName):
        currentFunction = interpreter.functions[funcName]
        for action in currentFunction.code:
            interpreter.next(action[0], *action[1:])

    @staticmethod
    def repeat(interpreter, cycle):
        if len(cycle) == 0:
            raise Exception(f"Конец цикла без начала")
        coords = []
        for i in range(cycle[-1][0]):
            for j in range(cycle[-1][0], interpreter.currentLine):
                coords.extend(interpreter.next(interpreter.code[j][0], *interpreter.code[j][1:]))
        return coords


class Interpreter:

    def __init__(self):
        self.functions = dict()
        self.variables = dict()
        self.code = []
        self.currentLine = 0
        self.cycles = []
        self.ifTrue = True
        self.x = 0
        self.y = 0
        self.saveProc = False
        self.currentProc = []
        self.currentProcName = ""
        self.ifMap = dict()
        self.funcMap = dict()
        self.stack = []

    def load(self, lines):
        stack = []
        for idx, line in enumerate(lines):
            if line[0] == "PROCEDURE":
                if len(stack) != 0:
                    raise Exception(f"Объявление процедуры внутри блока {stack[-1]} на {idx + 1}")
                if line[1] in self.funcMap:
                    raise Exception(f"Повторное объявление процедуры {line[1]} на {idx + 1}")
                self.funcMap[line[1]] = idx
                stack.append(("PROCEDURE", idx))
            if line[0] == "ENDPROC":
                if stack[-1][0] != "PROCEDURE":
                    raise Exception(f"Неожиданный ENDPROC на {idx + 1}")
                stack.pop()
            if line[0] == "IFBLOCK":
                if len(stack) > 2:
                    raise Exception(f"Слишком большая степень вложенности на {idx + 1}")
                stack.append(("IFBLOCK", idx))
            if line[0] == "ENDIF":
                if stack[-1][0] != "IFBLOCK":
                    raise Exception(f"Неожиданный ENDIF на {idx + 1}")
                self.ifMap[stack[-1][1]] = idx
                stack.pop()
            if line[0] == "REPEAT":
                if len(stack) > 2:
                    raise Exception(f"Слишком большая степень вложенности на {idx + 1}")
                stack.append(("REPEAT", idx))
            if line[0] == "ENDREPEAT":
                if stack[-1][0] != "REPEAT":
                    raise Exception(f"Неожиданный ENDREPEAT на {idx + 1}")
                stack.pop()


            self.code.append([line[0], *line[1:]])
        self.code.append(["ENDPROG"])
        self.code.append(["ENDPROG"])
        if len(stack) != 0:
            raise Exception(f"Незакрытый блок IF, PROCEDURE или REPEAT на {stack[-1][1]}")
        if __name__ == "__main__":
            print(self.code)
            print(self.ifMap)
            print(self.funcMap)
        return True

    def next(self):
        token = self.code[self.currentLine][0]
        args = self.code[self.currentLine][1:]
        match token:
            case "RIGHT" | "LEFT" | "UP" | "DOWN":
                if type(self.get_value(args[0])) != int:
                    raise Exception(
                        f"""Неверный тип аргумента 'расстояние' ожидается int, найдено"
{type(args[0])} на строке {self.currentLine}!""")
                if not (0 <= self.get_value(args[0]) <= 1000):
                    raise Exception(f"Неверное значение аргумента на строке {self.currentLine + 1}!")
                Actions.move(self, token, self.get_value(args[0]))
                if self.x < -10 or self.x > 10 or self.y < -10 or self.y > 10:
                    raise Exception("Исполнитель вышел за пределы поля!")
            case "IFBLOCK":
                if len(self.stack) > 2:
                    raise Exception(f"Слишком большая степень вложенности!")
                if not Actions.checkIf(self, args[0]):
                    self.currentLine = self.ifMap[self.currentLine]
                    self.currentLine += 1
                else:
                    self.currentLine += 1
                    if len(self.stack) > 2:
                        raise Exception(f"Слишком большая степень вложенности!")
                    self.stack.append(["IFBLOCK", self.currentLine])
                return self.next()
            case "ENDIF":
                if self.stack[-1][0] != "IFBLOCK":
                    raise Exception(f"ENDIF без соответствующего IFBLOCK")
                self.stack.pop()
                self.currentLine += 1
                return self.next()
            case "REPEAT":
                val = self.get_value(args[0])
                if type(val) != int:
                    raise Exception(
                        f"""Неверный аргумент 'количество итерраций', найдено"
                {type(args[0])} на строке {self.currentLine + 1}!""")
                if not (0 <= val <= 1000):
                    raise Exception(f"Неверное значение аргумента на строке {self.currentLine + 1}!")
                if val == 0:
                    raise Exception(f"Бесконечный цикл на строке {self.currentLine + 1}")
                if len(self.stack) > 2:
                    raise Exception(f"Слишком большая степень вложенности!")
                self.stack.append(["STARTFOR", self.currentLine + 1, val - 1])
                self.currentLine += 1
                return self.next()
                pass
            case "ENDREPEAT":
                if self.stack[-1][0] != "STARTFOR":
                    raise Exception(f"ENDREPEAT без соответствующего REPEAT")
                top = self.stack.pop()
                if top[2] > 0:
                    top[2] -= 1
                    self.currentLine = top[1]
                    self.stack.append(top)
                else:
                    self.currentLine += 1
                return self.next()
                pass
            case "SET":
                if type(self.get_value(args[1])) != int:
                    raise Exception(
                        f"""Неверный тип аргумента 'значение' ожидается int, найдено"
                {type(args[1])} на строке {self.currentLine + 1}!""")

                self.variables[args[0]] = self.get_value(args[1])
                self.currentLine += 1
                return self.next()
            case "PROCEDURE":
                while self.code[self.currentLine][0] != "ENDPROC" and self.code[self.currentLine][0] != "ENDPROG":
                    self.currentLine += 1
                self.currentLine += 1
                return self.next()
            case "ENDPROC":
                if self.stack[-1][0] != "STARTPROC":
                    raise Exception(f"ENDPROC без соответствующего PROCEDURE")
                self.currentLine = self.stack[-1][1]
                self.stack.pop()
                return self.next()
            case "CALL":
                if args[0] not in self.funcMap:
                    raise Exception(f"Использование необъявленной функции {args[0]} на строке {self.currentLine + 1}")
                if len(self.stack) > 2:
                    raise Exception(f"Слишком большая степень вложенности!")
                self.stack.append(["STARTPROC", self.currentLine + 1])
                self.currentLine = self.funcMap[args[0]] + 1
                return self.next()
            case "ENDPROG":
                return None
            case _:
                raise Exception(f"Неизвестный токен {token} на строке {self.currentLine + 1}!")
        self.currentLine += 1
        return [self.x, self.y]

    def get_value(self, val):
        try:
            val = int(val)
        except Exception as e:
            pass
        if type(val) == int:
            return val
        if val not in self.variables:
            raise Exception(f"Использование необъявленной переменной {val} на {self.currentLine + 1}")
        return self.variables[val]


if __name__ == "__main__":
    interpret = Interpreter()
    interpret.load(
        [["SET", "X", 0], ["RIGHT", 10], ["IF", "RIGHT"], ["LEFT", 10], ["ENDIF"], ["PROCEDURE", "TEST"], ["RIGHT", 2],
         ["UP", 2], ["ENDPROC"],
         ["REPEAT", "X"], ["CALL", "TEST"], ["ENDREPEAT"]])
    for i in range(15):
        print(interpret.next())
