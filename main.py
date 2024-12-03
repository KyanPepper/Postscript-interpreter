import ast  
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
                self.stack.append(command[1:])  # Store key without `/` for as a definition
            elif command.isdigit() or (command[0] == '-' and command[1:].isdigit()):
                self.stack.append(int(command))
            elif command == "True":
                self.stack.append(True)
            elif command == "False":
                self.stack.append(False)
            else:
                # Check if the string can be safely parsed as a list or other literal 
                # found https://stackoverflow.com/questions/52232742/how-to-use-ast-literal-eval-in-a-pandas-dataframe-and-handle-exceptions/56842372
                try:
                    value = ast.literal_eval(command)
                    if isinstance(command, (list, str)):
                        self.stack.append(value)
                    else:
                        self.stack.append(command)
                except (ValueError, SyntaxError):
                    value = self.lookup(command)
                    if value is not None:
                        self.stack.append(value)
                    else:
                        self.stack.append(command)
        else:
            self.stack.append(command)


    # Resolves a variable name to its value considering scoping type
    def lookup(self, name):
        if self.use_lexical_scoping:
            # For lexical scoping, search from the innermost to the outermost scope
            for d in reversed(self.dict_stack):
                if name in d:
                    return d[name]
        else:
            # For dynamic scoping, search from the outermost to the innermost scope
            for d in self.dict_stack:
                if name in d:
                    return d[name]
        return None

    def def_(self):
        value = self.stack.pop()
        key = self.stack.pop()
        if not isinstance(key, str):
            raise TypeError("Key for def must be a string")

        if self.use_lexical_scoping:
            # Always define in the top-most dictionary in the stack for lexical scoping
            self.dict_stack[-1][key] = value
        else:
            # For dynamic scoping, define in the first dictionary where the key doesn't exist or at the top-most
            for d in self.dict_stack:
                if key in d:
                    d[key] = value
                    return
            self.dict_stack[-1][key] = value  # Define in the top-most dictionary if not found elsewhere

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def exch(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to exchange")
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def pop(self):
        if not self.stack:
            raise IndexError("Stack underflow: no elements to pop")
        self.stack.pop()

    def dup(self):
        if not self.stack:
            raise IndexError("Stack underflow: no elements to duplicate")
        self.stack.append(self.stack[-1])

    def clear(self):
        self.stack.clear()

    def count(self):
        self.stack.append(len(self.stack))

    def add(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to add")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a + b)

    def sub(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to subtract")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a - b)

    def mul(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to multiply")
        self.stack.append(self.stack.pop() * self.stack.pop())

    def div(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to divide")
        b, a = self.stack.pop(), self.stack.pop()
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        self.stack.append(a / b)

    def idiv(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to integer divide")
        b, a = self.stack.pop(), self.stack.pop()
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        self.stack.append(a // b)

    def mod(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to modulo")
        b, a = self.stack.pop(), self.stack.pop()
        if b == 0:
            raise ZeroDivisionError("Modulo by zero")
        self.stack.append(a % b)

    def abs(self):
        if not self.stack:
            raise IndexError("Stack underflow: no elements to apply abs")
        self.stack.append(abs(self.stack.pop()))

    def neg(self):
        if not self.stack:
            raise IndexError("Stack underflow: no elements to negate")
        self.stack.append(-self.stack.pop())

    def ceiling(self):
        if not self.stack:
            raise IndexError("Stack underflow: no elements to apply ceiling")
        self.stack.append(int(float(self.stack.pop()) + 0.999999))

    def floor(self):
        if not self.stack:
            raise IndexError("Stack underflow: no elements to apply floor")
        self.stack.append(int(float(self.stack.pop())))

    def round(self):
        if not self.stack:
            raise IndexError("Stack underflow: no elements to apply round")
        self.stack.append(round(float(self.stack.pop())))

    def sqrt(self):
        if not self.stack:
            raise IndexError("Stack underflow: no elements to apply sqrt")
        self.stack.append(float(self.stack.pop()) ** 0.5)

    def dict(self):
        self.stack.append({})

    def length(self):
        if not self.stack:
            raise IndexError("Stack underflow: no elements to apply length")
        top = self.stack.pop()
        if not isinstance(top, (str, list)):
            raise TypeError("Operand must be a string or list to get length")
        self.stack.append(len(top))

    def begin(self):
        if not self.stack:
            raise IndexError("Stack underflow: no element to begin with")
        self.dict_stack.append(self.stack.pop())

    def end(self):
        if len(self.dict_stack) <= 1:
            raise IndexError("Cannot pop the global dictionary")
        self.dict_stack.pop()

    def eq(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to compare")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a == b)

    def ne(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to compare")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a != b)

    def gt(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to compare")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a > b)
        
    def lt(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to compare")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a < b)

    def and_(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to apply 'and'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(bool(a) and bool(b))

    def or_(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements to apply 'or'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(bool(a) or bool(b))

    def not_(self):
        if not self.stack:
            raise IndexError("Stack underflow: no element to apply 'not'")
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
        if not self.stack:
            print("Stack is empty")
        print(self.stack.pop())

    def if_(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements for 'if'")
        block, condition = self.stack.pop(), self.stack.pop()
        if condition:
            self.execute(block)


    
    def ifelse(self):
        if len(self.stack) < 3:
            raise IndexError("Stack underflow: not enough elements for 'ifelse'")
        false_block, true_block, condition = self.stack.pop(), self.stack.pop(), self.stack.pop()
        if condition:
            self.execute(true_block)
        else:
            self.execute(false_block)

    def copy(self):
        if not self.stack:
            raise IndexError("Stack underflow: no elements to copy")
        n = self.stack.pop()
        if not isinstance(n, int) or n < 0:
            raise TypeError("Invalid argument: 'copy' requires a non-negative integer")
        if n > len(self.stack):
            raise IndexError("Stack underflow: not enough elements to copy")
        # Copy the top n elements onto the stack
        self.stack.extend(self.stack[-n:])
    def get(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements for 'get'")
        index, container = self.stack.pop(), self.stack.pop()
        if isinstance(container, (str, list)):
            self.stack.append(container[index])
        else:
            raise TypeError("Invalid type for 'get': expected string or list")

    def getinterval(self):
        if len(self.stack) < 3:
            raise IndexError("Stack underflow: not enough elements for 'getinterval'")
        count, index, container = self.stack.pop(), self.stack.pop(), self.stack.pop()
        if isinstance(container, str):
            self.stack.append(container[index:index + count])
        elif isinstance(container, list):
            self.stack.append(container[index:index + count])
        else:
            raise TypeError("Invalid type for 'getinterval': expected string or list")

    def putinterval(self):
        if len(self.stack) < 3:
            raise IndexError("Stack underflow: not enough elements for 'putinterval'")
        substring, index, container = self.stack.pop(), self.stack.pop(), self.stack.pop()
        if isinstance(container, str):
            container = list(container)  # Strings are immutable, so we convert to list for modification
            container[index:index + len(substring)] = list(substring)
            self.stack.append(''.join(container))  # Convert back to string
        elif isinstance(container, list):
            container[index:index + len(substring)] = substring
            self.stack.append(container)
        else:
            raise TypeError("Invalid type for 'putinterval': expected string or list")

    def for_(self):
        if len(self.stack) < 4:
            raise IndexError("Stack underflow: not enough elements for 'for'")
        proc, end, step, start = self.stack.pop(), self.stack.pop(), self.stack.pop(), self.stack.pop()
        if not callable(proc):
            raise TypeError("Invalid type for 'for': procedure must be callable")
        for i in range(start, end + 1, step):
            self.stack.append(i)
            self.execute(proc)

    def repeat(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements for 'repeat'")
        proc, count = self.stack.pop(), self.stack.pop()
        if not callable(proc):
            raise TypeError("Invalid type for 'repeat': procedure must be callable")
        for _ in range(count):
            self.execute(proc)

    def quit(self):
        raise SystemExit("PostScript interpreter terminated by 'quit' command")

    def eq(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements for 'eq'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a == b)

    def ne(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements for 'ne'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a != b)

    def ge(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements for 'ge'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a >= b)

    def le(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements for 'le'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a <= b)

    def print_(self):
        if not self.stack:
            print("Stack is empty")
        print(self.stack.pop())

    def eq(self):
        if len(self.stack) < 2:
            raise IndexError("Stack underflow: not enough elements for 'eq'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a == b)

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
            "ge": self.ge,
            "lt": self.lt,
            "le": self.le,
            "and": self.and_,
            "or": self.or_,
            "not": self.not_,
            "true": self.true,
            "false": self.false,
            "get": self.get,
            "getinterval": self.getinterval,
            "putinterval": self.putinterval,
            "ifelse": self.ifelse,
            "if": self.if_,
            "for": self.for_,
            "repeat": self.repeat,
            "quit": self.quit,
            "print": self.print_,
        }