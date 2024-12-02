class PostScriptInterpreter:
    def __init__(self, use_lexical_scoping=False):
        self.stack = []
        self.dict_stack = [{}]
        self.use_lexical_scoping = use_lexical_scoping

    def execute(self, command):
        if isinstance(command, list):
            for cmd in command:
                self.execute(cmd)
        elif isinstance(command, str):
            if command in self.commands():
                self.commands()[command]()
            elif command.startswith("/"):
                self.stack.append(command[1:])  # Store key without `/`
            elif command.isdigit() or (command[0] == '-' and command[1:].isdigit()):
                self.stack.append(int(command))
            elif command == "True":
                self.stack.append(True)
            elif command == "False":
                self.stack.append(False)
            else:
                for d in reversed(self.dict_stack):
                    if command in d:
                        self.stack.append(d[command])
                        return
                self.stack.append(command)
        else:
            self.stack.append(command)
        
    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def exch(self):
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def pop(self):
        self.stack.pop()

    def copy(self):
        n = self.stack.pop()
        self.stack.extend(self.stack[-n:])

    def dup(self):
        self.stack.append(self.stack[-1])

    def clear(self):
        self.stack.clear()

    def count(self):
        self.stack.append(len(self.stack))

    def add(self):
        self.stack.append(self.stack.pop() + self.stack.pop())

    def sub(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a - b)

    def mul(self):
        self.stack.append(self.stack.pop() * self.stack.pop())

    def div(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a / b)

    def idiv(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a // b)

    def mod(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a % b)

    def abs(self):
        self.stack.append(abs(self.stack.pop()))

    def neg(self):
        self.stack.append(-self.stack.pop())

    def ceiling(self):
        self.stack.append(int(float(self.stack.pop()) + 0.999999))

    def floor(self):
        self.stack.append(int(float(self.stack.pop())))

    def round(self):
        self.stack.append(round(float(self.stack.pop())))

    def sqrt(self):
        self.stack.append(float(self.stack.pop()) ** 0.5)

    def dict(self):
        self.stack.append({})

    def length(self):
        top = self.stack.pop()
        if isinstance(top, str) and top.startswith("[") and top.endswith("]"):
            top = eval(top)
        self.stack.append(len(top))

    def begin(self):
        self.dict_stack.append(self.stack.pop())

    def end(self):
        self.dict_stack.pop()

    def def_(self):
        value = self.stack.pop()
        key = self.stack.pop()
        if not isinstance(key, str):
            raise TypeError("Key for def must be a string")
        if self.use_lexical_scoping:
            self.dict_stack[-1][key] = value
        else:
            for d in reversed(self.dict_stack):
                if key in d:
                    d[key] = value
                    return
            self.dict_stack[-1][key] = value

    def eq(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a == b)

    def ne(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a != b)

    def gt(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a > b)

    def lt(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a < b)

    def and_(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(bool(a) and bool(b))

    def or_(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(bool(a) or bool(b))

    def not_(self):
        value = self.stack.pop()
        if isinstance(value, bool):
            self.stack.append(not value)
        else:
            raise TypeError("Operand for 'not' must be a boolean")


    def true(self):
        self.stack.append(True)

    def false(self):
        self.stack.append(False)

    def print_(self):
        print(self.stack.pop())

    def commands(self):
        return {
            "exch": self.exch,
            "pop": self.pop,
            "copy": self.copy,
            "dup": self.dup,
            "clear": self.clear,
            "count": self.count,
            "add": self.add,
            "sub": self.sub,
            "mul": self.mul,
            "div": self.div,
            "idiv": self.idiv,
            "mod": self.mod,
            "abs": self.abs,
            "neg": self.neg,
            "ceiling": self.ceiling,
            "floor": self.floor,
            "round": self.round,
            "sqrt": self.sqrt,
            "dict": self.dict,
            "length": self.length,
            "begin": self.begin,
            "end": self.end,
            "def": self.def_,
            "eq": self.eq,
            "ne": self.ne,
            "gt": self.gt,
            "lt": self.lt,
            "and": self.and_,
            "or": self.or_,
            "not": self.not_,
            "true": self.true,
            "false": self.false,
            "print": self.print_,
        }
