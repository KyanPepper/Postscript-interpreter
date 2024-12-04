import ast

class PostScriptInterpreter:
    """
    A class to represent a PostScript interpreter.
    Attributes
    stack : list
        Operand stack.
    dict_stack : list
        Dictionary stack.
    use_lexical_scoping : bool
        Flag to determine if lexical scoping is used.
        
    Methods
    execute(command):
        Executes the user command in the stack.
    lookup(name):
        Looks up the value of a name in the dictionary stack.
    def_():
        Defines a new key-value pair in the dictionary stack.
    is_float(value):
        Checks if a value can be converted to a float.
    exch():
        Exchanges the top two elements on the stack.
    pop():
        Removes the top element from the stack.
    dup():
        Duplicates the top element on the stack.
    clear():
        Clears the stack.
    count():
        Pushes the number of elements in the stack onto the stack.
    add():
        Adds the top two elements on the stack.
    sub():
        Subtracts the top two elements on the stack.
    mul():
        Multiplies the top two elements on the stack.
    div():
        Divides the top two elements on the stack.
    idiv():
        Performs integer division on the top two elements on the stack.
    mod():
        Computes the modulo of the top two elements on the stack.
    abs():
        Computes the absolute value of the top element on the stack.
    neg():
        Negates the top element on the stack.
    ceiling():
        Computes the ceiling of the top element on the stack.
    floor():
        Computes the floor of the top element on the stack.
    round():
        Rounds the top element on the stack.
    sqrt():
        Computes the square root of the top element on the stack.
    dict():
        Pushes an empty dictionary onto the stack.
    length():
        Pushes the length of the top element on the stack.
    begin():
        Begins a new dictionary scope.
    end():
        Ends the current dictionary scope.
    eq():
        Checks if the top two elements on the stack are equal.
    ne():
        Checks if the top two elements on the stack are not equal.
    gt():
        Checks if the second element on the stack is greater than the top element.
    lt():
        Checks if the second element on the stack is less than the top element.
    ge():
        Checks if the second element on the stack is greater than or equal to the top element.
    le():
        Checks if the second element on the stack is less than or equal to the top element.
    and_():
        Computes the logical AND of the top two elements on the stack.
    or_():
        Computes the logical OR of the top two elements on the stack.
    not_():
        Computes the logical NOT of the top element on the stack.
    true():
        Pushes True onto the stack.
    false():
        Pushes False onto the stack.
    print_():
        Prints the top element on the stack.
    if_():
        Executes a block if the top element on the stack is True.
    ifelse():
        Executes one of two blocks based on the top element on the stack.
    copy():
        Copies the top n elements on the stack.
    get():
        Gets an element from a container on the stack.
    getinterval():
        Gets a subinterval from a container on the stack.
    putinterval():
        Replaces a subinterval in a container on the stack.
    repeat():
        Repeats a procedure a specified number of times.
    quit():
        Terminates the interpreter.
    put():
        Puts a value into a container at a specified index.
    forall():
        Applies a procedure to each element in a container.
    for_():
        Executes a procedure for a range of values.
    commands():
        Returns a dictionary of command names to methods.
    """
    def __init__(self, use_lexical_scoping=False):
        self.stack = []  # Operand stack
        self.dict_stack = [{}]  # Dictionary stack
        self.use_lexical_scoping = use_lexical_scoping  # Scoping flag

#Excute the  user command in the stack
    def execute(self, command):
        if isinstance(command, list):
            for cmd in command:
                self.execute(cmd)
        elif isinstance(command, str):
            if command in self.commands():
                self.commands()[command]()
            elif command.startswith("/"):
                self.stack.append(command[1:])  # Store key without `/` for definition
            elif command.isdigit() or (command[0] == '-' and command[1:].isdigit()):
                self.stack.append(int(command))
            elif command == "True":
                self.stack.append(True)
            elif command == "False":
                self.stack.append(False)
            else:
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

#Look up the value of a name in the dictionary stack
    def lookup(self, name):
        if self.use_lexical_scoping:
            if name in self.dict_stack[-1]:
                return self.dict_stack[-1][name]
        else:
            for d in reversed(self.dict_stack):
                if name in d:
                    return d[name]
        return None

#Define a new key-value pair in the dictionary stack
    def def_(self):
        value = self.stack.pop()
        key = self.stack.pop()
        if not isinstance(key, str):
            raise TypeError("The key for 'def' must be a string")

        if self.use_lexical_scoping:
            self.dict_stack[-1][key] = value
        else:
            for d in self.dict_stack:
                if key in d:
                    d[key] = value
                    return
            self.dict_stack[-1][key] = value

#Check if a value can be converted to a float throw an exception if it can't
    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

#Exchange the top two elements on the stack
    def exch(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to exchange")
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

#Remove the top element from the stack
    def pop(self):
        if not self.stack:
            raise IndexError("No elements to pop")
        self.stack.pop()

#Duplicate the top element on the stack
    def dup(self):
        if not self.stack:
            raise IndexError("No elements to duplicate")
        self.stack.append(self.stack[-1])

#Clear the stack
    def clear(self):
        self.stack.clear()

#Push the number of elements in the stack onto the stack
    def count(self):
        self.stack.append(len(self.stack))

#Add the top two elements on the stack
    def add(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to add")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a + b)

#Subtract the top two elements on the stack
    def sub(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to subtract")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a - b)

#Multiply the top two elements on the stack
    def mul(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to multiply")
        self.stack.append(self.stack.pop() * self.stack.pop())

#Divide the top two elements on the stack
    def div(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to divide")
        b, a = self.stack.pop(), self.stack.pop()
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        self.stack.append(a / b)

#Perform integer division on the top two elements on the stack
    def idiv(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to perform integer division")
        b, a = self.stack.pop(), self.stack.pop()
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        self.stack.append(a // b)

#Compute the remainder of the top two elements on the stack
    def mod(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to perform modulo operation")
        b, a = self.stack.pop(), self.stack.pop()
        if b == 0:
            raise ZeroDivisionError("Cannot perform modulo by zero")
        self.stack.append(a % b)

#Compute the absolute value of the top element on the stack
    def abs(self):
        if not self.stack:
            raise IndexError("No elements to apply abs")
        self.stack.append(abs(self.stack.pop()))

#Negate the top element on the stack
    def neg(self):
        if not self.stack:
            raise IndexError("No elements to negate")
        self.stack.append(-self.stack.pop())

#Compute the ceiling of the top element on the stack
    def ceiling(self):
        if not self.stack:
            raise IndexError("No elements to apply ceiling")
        self.stack.append(int(float(self.stack.pop()) + 0.999999))

#Compute the floor of the top element on the stack
    def floor(self):
        if not self.stack:
            raise IndexError("No elements to apply floor")
        self.stack.append(int(float(self.stack.pop())))

#Round the top element on the stack
    def round(self):
        if not self.stack:
            raise IndexError("No elements to apply round")
        self.stack.append(round(float(self.stack.pop())))

#Compute the square root of the top element on the stack
    def sqrt(self):
        if not self.stack:
            raise IndexError("No elements to apply sqrt")
        self.stack.append(float(self.stack.pop()) ** 0.5)

#Push an empty dictionary onto the stack
    def dict(self):
        self.stack.append({})

#Push the length of the top element on the stack
    def length(self):
        if not self.stack:
            raise IndexError("No elements to get length")
        top = self.stack.pop()
        if not isinstance(top, (str, list)):
            raise TypeError("Operand must be a string or list to get length")
        self.stack.append(len(top))

#Begin a new dictionary scope
    def begin(self):
        if not self.stack:
            raise IndexError("No element to begin with")
        self.dict_stack.append(self.stack.pop())

#End the current dictionary scope
    def end(self):
        if len(self.dict_stack) <= 1:
            raise IndexError("Cannot pop the global dictionary")
        self.dict_stack.pop()

#Check if the top two elements on the stack are equal
    def eq(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to compare")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a == b)

#Check if the top two elements on the stack are not equal
    def ne(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to compare")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a != b)

#Check if the second element on the stack is greater than the top element
    def gt(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to compare")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a > b)
        
#Check if the second element on the stack is less than the top element
    def lt(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to compare")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a < b)

#Check if the second element on the stack is greater than or equal to the top element
    def and_(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to apply 'and'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(bool(a) and bool(b))

#Compute the logical OR of the top two elements on the stack
    def or_(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements to apply 'or'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(bool(a) or bool(b))

#Compute the logical NOT of the top element on the stack
    def not_(self):
        if not self.stack:
            raise IndexError("No element to apply 'not'")
        value = self.stack.pop()
        if isinstance(value, bool):
            self.stack.append(not value)
        else:
            raise TypeError("Operand for 'not' must be a boolean")

#Push True onto the stack (should be obivous)
    def true(self):
        self.stack.append(True)

#Push False onto the stack (should be obivous)
    def false(self):
        self.stack.append(False)

#Print the top element on the stack
    def print_(self):
        if not self.stack:
            print("Stack is empty")
        print(self.stack.pop())

#Execute a block if the top element on the stack is True
    def if_(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements for 'if'")
        block, condition = self.stack.pop(), self.stack.pop()
        if condition:
            self.execute(block)

#if the top element on the stack is True, execute the first block, otherwise execute the second block
    def ifelse(self):
        if len(self.stack) < 3:
            raise IndexError("Not enough elements for 'ifelse'")
        false_block, true_block, condition = self.stack.pop(), self.stack.pop(), self.stack.pop()
        if condition:
            self.execute(true_block)
        else:
            self.execute(false_block)

#Copy the top n elements on the stack
    def copy(self):
        if not self.stack:
            raise IndexError("No elements to copy")
        n = self.stack.pop()
        if not isinstance(n, int) or n < 0:
            raise TypeError("Invalid argument: 'copy' requires a non-negative integer")
        if n > len(self.stack):
            raise IndexError("Not enough elements to copy")
        self.stack.extend(self.stack[-n:])
        
#Get an element from a container on the stack
    def get(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements for 'get'")
        index, container = self.stack.pop(), self.stack.pop()
        if isinstance(container, (str, list)):
            self.stack.append(container[index])
        else:
            raise TypeError("Invalid type for 'get': expected string or list")

#Get a subinterval from a container on the stack
    def getinterval(self):
        if len(self.stack) < 3:
            raise IndexError("Not enough elements for 'getinterval'")
        count, index, container = self.stack.pop(), self.stack.pop(), self.stack.pop()
        if isinstance(container, str):
            self.stack.append(container[index:index + count])
        elif isinstance(container, list):
            self.stack.append(container[index:index + count])
        else:
            raise TypeError("Invalid type for 'getinterval': expected string or list")

#Replace a subinterval in a container on the stack
    def putinterval(self):
        if len(self.stack) < 3:
            raise IndexError("Not enough elements for 'putinterval'")
        substring, index, container = self.stack.pop(), self.stack.pop(), self.stack.pop()
        if isinstance(container, str):
            container = list(container)
            container[index:index + len(substring)] = list(substring)
            self.stack.append(''.join(container))
        elif isinstance(container, list):
            container[index:index + len(substring)] = substring
            self.stack.append(container)
        else:
            raise TypeError("Invalid type for 'putinterval': expected string or list")

#Repeat a procedure a specified number of times
    def repeat(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements for 'repeat'")
        proc, count = self.stack.pop(), self.stack.pop()
        if not callable(proc):
            raise TypeError("Invalid type for 'repeat': procedure must be callable")
        for _ in range(count):
            self.execute(proc)

#Terminate the interpreter
    def quit(self):
        raise SystemExit("PostScript interpreter terminated by 'quit' command")

#Return a dictionary of command names to methods
    def eq(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements for 'eq'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a == b)

#Apply a procedure to each element in a container
    def ne(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements for 'ne'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a != b)

#Execute a procedure for a range of values
    def ge(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements for 'ge'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a >= b)

#Execute a procedure for a range of values
    def le(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements for 'le'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a <= b)


#Return a dictionary of command names to methods
    def eq(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements for 'eq'")
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a == b)

#replace a value in a container on the stack
    def put(self):
        if len(self.stack) < 3:
            raise IndexError("Not enough elements for 'put'")
        value, index, container = self.stack.pop(), self.stack.pop(), self.stack.pop()
        if isinstance(container, list):
            if 0 <= index < len(container):
                container[index] = value
            else:
                raise IndexError("Index out of range for 'put'")
            self.stack.append(container)
        elif isinstance(container, str):
            container = list(container)
            container[index] = value
            self.stack.append(''.join(container))
        else:
            raise TypeError("Invalid type for 'put': expected list or string")
        
#Apply a procedure to each element in a container
    def forall(self):
        if len(self.stack) < 2:
            raise IndexError("Not enough elements for 'forall'")
        proc, container = self.stack.pop(), self.stack.pop()
        if not callable(proc):
            raise TypeError("Invalid type for 'forall': procedure must be callable")
        if isinstance(container, (str, list)):
            for item in container:
                self.stack.append(item)
                self.execute(proc)
        else:
            raise TypeError("Invalid type for 'forall': expected string or list")
        
#For a range of values, execute a procedure
    def for_(self): 
        if len(self.stack) < 4:
            raise IndexError("Not enough elements for 'for'")
        proc, end, step, start = self.stack.pop(), self.stack.pop(), self.stack.pop(), self.stack.pop()
        if not callable(proc):
            raise TypeError("Invalid type for 'for': procedure must be callable")
        for i in range(start, end + 1, step):
            self.stack.append(i)
            self.execute(proc)

#Return a dictionary of command names to methods
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
            "put": self.put,
            "ifelse": self.ifelse,
            "if": self.if_,
            "for": self.for_,
            "repeat": self.repeat,
            "quit": self.quit,
            "print": self.print_,
            "exit": self.quit,
            "stop": self.quit,
            "forall": self.forall
        }
