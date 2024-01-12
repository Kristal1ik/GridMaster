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
                    interpreter.ifTrue = False
            case "LEFT":
                if interpreter.x != -10:
                    interpreter.ifTrue = False
            case "UP":
                if interpreter.y != 10:
                    interpreter.ifTrue = False
            case "DOWN":
                if interpreter.y != -10:
                    interpreter.ifTrue = False
            case _:
                raise Exception(f"Неизвестное направление {direction}")

    @staticmethod
    def call(interpreter, funcName):
        currentFunction = interpreter.functions[funcName]
        for action in currentFunction:
            interpreter.next(action[0], action[1])

    @staticmethod
    def repeat(interpreter, cycle):
        if len(cycle) == 0:
            raise Exception(f"Конец цикла без начала")
        coords = []
        for i in range(cycle.top()[1]):
            for j in range(cycle.top[0], interpreter.currentLine):
                coords.extend(interpreter.next(interpreter.code[j][0], interpreter.code[j][1]))
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

    def next(self, token, *args):
        if not self.ifTrue:
            if token != "ENDIF":
                return self.x, self.y
            else:
                self.ifTrue = True
        if self.saveProc:
            if self.currentProcName == "":
                self.currentProcName = args[0]
            if token != "ENDPROC":
                self.currentProc.append((token, [args]))
            else:
                self.saveProc = False
                self.functions[self.currentProcName] = Function(self.currentProcName, self.currentProc)

        match token:
            case "RIGHT" | "LEFT" | "UP" | "DOWN":
                if type(self.get_value(args[0])) != int:
                    raise Exception(
                        f"""Неверный тип аргумента 'расстояние' ожидается int, найдено"
{type(args[0])} на строке {self.currentLine}!""")
                Actions.move(self, token, self.get_value(args[0]))
                if self.x < -10 or self.x > 10 or self.y < -10 or self.y > 10:
                    raise Exception("Исполнитель вышел за пределы поля!")
            case "IFBLOCK":
                Actions.checkIf(self, args[0])
            case "ENDIF":
                pass
            case "REPEAT":
                if type(self.get_value(args[0])) != int:
                    raise Exception(
                        f"""Неверный аргумент 'количество итерраций', найдено"
                {type(args[0])} на строке {self.currentLine}!""")
                self.cycles.append([self.currentLine, self.get_value(args[0])])
                pass
            case "ENDREPEAT":
                Actions.repeat(self, self.cycles)
                pass
            case "SET":
                if type(self.get_value(args[1])) != int:
                    raise Exception(
                        f"""Неверный тип аргумента 'значение' ожидается int, найдено"
                {type(args[0])} на строке {self.currentLine}!""")
                self.variables[args[0]] = self.get_value(args[1])
            case "PROCEDURE":
                self.saveProc = True
                self.currentProcName = args[0]
            case "ENDPROC":
                self.saveProc = False
            case "CALL":
                if args[0] not in self.functions:
                    raise Exception(f"Использование необъявленной функции {args[0]} на строке {self.currentLine}")
                Actions.call(self, args[0])
            case _:
                raise Exception(f"Неизвестный токе {token} на строке {self.currentLine}!")
        self.currentLine += 1
        self.code.append((token, [args]))
        return [[self.x, self.y]]

    def get_value(self, val):
        if type(val) == int:
            return val
        if val in self.variables:
            raise Exception(f"Использование необъявленной переменной {val} на {self.currentLine}")
        return self.variables[val]
