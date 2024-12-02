class PostScriptInterpreter:
    def __init__(self, use_lexical_scoping=False):
        # Initialize the operand stack and the dictionary stack
        self.stack = []
        self.dict_stack = [{}]
        self.use_lexical_scoping = use_lexical_scoping

    def execute(self, command):
        # Execute a list of commands or a single command
        if isinstance(command, list):
            for cmd in command:
                self.execute(cmd)
        elif isinstance(command, str):
            if command in self.commands():
                self.commands()[command]()
            elif command.isdigit() or (command[0] == '-' and command[1:].isdigit()):
                self.stack.append(int(command))
            else:
                self.stack.append(command)
        else:
            self.stack.append(command)

    def exch(self):
        # Exchange the top two elements on the stack
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def pop(self):
        # Pop the top element from the stack
        self.stack.pop()

    def copy(self):
        # Copy the top n elements on the stack
        n = self.stack.pop()
        self.stack.extend(self.stack[-n:])

    def dup(self):
        # Duplicate the top element on the stack
        self.stack.append(self.stack[-1])

    def clear(self):
        # Clear the stack
        self.stack.clear()

    def count(self):
        # Push the number of elements on the stack
        self.stack.append(len(self.stack))

    def add(self):
        # Add the top two elements on the stack
        self.stack.append(self.stack.pop() + self.stack.pop())

    def sub(self):
        # Subtract the top element from the second top element on the stack
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a - b)

    def mul(self):
        # Multiply the top two elements on the stack
        self.stack.append(self.stack.pop() * self.stack.pop())

    def div(self):
        # Divide the second top element by the top element on the stack
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a / b)

    def idiv(self):
        # Integer divide the second top element by the top element on the stack
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a // b)

    def mod(self):
        # Modulo the second top element by the top element on the stack
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a % b)

    def abs(self):
        # Push the absolute value of the top element on the stack
        self.stack.append(abs(self.stack.pop()))

    def neg(self):
        # Negate the top element on the stack
        self.stack.append(-self.stack.pop())

    def ceiling(self):
        # Push the ceiling of the top element on the stack
        self.stack.append(int(self.stack.pop() + 0.999999))

    def floor(self):
        # Push the floor of the top element on the stack
        self.stack.append(int(self.stack.pop()))

    def round(self):
        # Push the rounded value of the top element on the stack
        self.stack.append(round(self.stack.pop()))

    def sqrt(self):
        # Push the square root of the top element on the stack
        self.stack.append(self.stack.pop() ** 0.5)

    def dict(self):
        # Push an empty dictionary onto the stack
        self.stack.append({})

    def length(self):
        # Push the length of the top element on the stack
        self.stack.append(len(self.stack.pop()))

    def maxlength(self):
        # Push the length of the top element on the stack (same as length)
        self.stack.append(len(self.stack.pop()))

    def begin(self):
        # Begin a new dictionary scope
        self.dict_stack.append(self.stack.pop())

    def end(self):
        # End the current dictionary scope
        self.dict_stack.pop()

    def def_(self):
        # Define a new key-value pair in the current dictionary scope
        value = self.stack.pop()
        key = self.stack.pop()
        if self.use_lexical_scoping:
            self.dict_stack[-1][key] = value
        else:
            for d in reversed(self.dict_stack):
                if key in d:
                    d[key] = value
                    return
            self.dict_stack[-1][key] = value

    def eq(self):
        # Push True if the top two elements are equal, else False
        self.stack.append(self.stack.pop() == self.stack.pop())

    def ne(self):
        # Push True if the top two elements are not equal, else False
        self.stack.append(self.stack.pop() != self.stack.pop())

    def ge(self):
        # Push True if the second top element is greater than or equal to the top element, else False
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a >= b)

    def gt(self):
        # Push True if the second top element is greater than the top element, else False
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a > b)

    def le(self):
        # Push True if the second top element is less than or equal to the top element, else False
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a <= b)

    def lt(self):
        # Push True if the second top element is less than the top element, else False
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a < b)

    def and_(self):
        # Push the logical AND of the top two elements on the stack
        self.stack.append(self.stack.pop() & self.stack.pop())

    def or_(self):
        # Push the logical OR of the top two elements on the stack
        self.stack.append(self.stack.pop() | self.stack.pop())

    def not_(self):
        # Push the logical NOT of the top element on the stack
        self.stack.append(not self.stack.pop())

    def true(self):
        # Push True onto the stack
        self.stack.append(True)

    def false(self):
        # Push False onto the stack
        self.stack.append(False)

    def print_(self):
        # Print the top element on the stack
        print(self.stack.pop())

    def eq_(self):
        # Print the top element on the stack (same as print_)
        print(self.stack.pop())

    def commands(self):
        # Return a dictionary of command names to methods
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
            "maxlength": self.maxlength,
            "begin": self.begin,
            "end": self.end,
            "def": self.def_,
            "eq": self.eq,
            "ne": self.ne,
            "ge": self.ge,
            "gt": self.gt,
            "le": self.le,
            "lt": self.lt,
            "and": self.and_,
            "or": self.or_,
            "not": self.not_,
            "true": self.true,
            "false": self.false,
            "print": self.print_,
            "=": self.eq_,
        }
    

