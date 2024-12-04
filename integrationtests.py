import pytest # type: ignore
from main import PostScriptInterpreter

@pytest.fixture
def interpreter():
    return PostScriptInterpreter(use_lexical_scoping=False)

@pytest.fixture
def interpreter_lexical():
    return PostScriptInterpreter(use_lexical_scoping=True)

def test_integration_arithmetic_and_logic(interpreter):
    commands = [
        "5", "3", "add",          # 5 + 3 = 8
        "2", "mul",               # 8 * 2 = 16
        "10", "lt",               # 16 < 10 -> False
        "true", "and"             # False AND True -> False
    ]
    interpreter.execute(commands)
    assert interpreter.stack == [False]

def test_integration_define_and_lookup(interpreter):
    commands = [
        "/x", "42", "def",       # Define x = 42
        "/y", "58", "def",       # Define y = 58
        "x", "y", "add"          # Push x and y, then add (42 + 58 = 100)
    ]
    interpreter.execute(commands)
    assert interpreter.stack == [100]

def test_integration_scoping_dynamic(interpreter):
    commands = [
        "/x", "42", "def",       # Define x = 42
        "dict", "begin",         # Start a new dictionary
        "/x", "100", "def",      # Define x = 100 in the new scope
        "x",                     # Should find x = 100 
        "end",                   # End the new dictionary scope
        "x"                      # Should still find x = 100 
    ]
    interpreter.execute(commands)
    assert interpreter.stack == [100, 100]

def test_integration_scoping_lexical(interpreter_lexical):
    commands = [
        "/x", "42", "def",       # Define x = 42
        "dict", "begin",         # Start a new dictionary
        "/x", "100", "def",      # Define x = 100 in the new scope
        "x",                     # Should find x = 100 (inner scope)
        "end",                   # End the new dictionary scope
        "x"                      # Should find x = 42 (outer scope)
    ]
    interpreter_lexical.execute(commands)
    assert interpreter_lexical.stack == [100, 42]

def test_integration_conditionals(interpreter):
    commands = [
        "5", "3", "lt",         # 5 < 3 -> False
        "10",                   # Push 10 if true
        "20",                   # Push 20 if false
        "ifelse"                # Execute the conditional
    ]
    interpreter.execute(commands)
    assert interpreter.stack == [20]

def test_integration_complex_stack_operations(interpreter):
    commands = [
        "1", "2", "3",           # Push 1, 2, 3
        "3", "copy",             # Copy top 3 elements
        "exch",                  # Swap top two elements
        "count"                  # Count elements in the stack
    ]
    interpreter.execute(commands)
    assert interpreter.stack == [1, 2, 3, 1, 3, 2, 6]

def test_integration_boolean_logic(interpreter):
    commands = [
        "true", "false", "or",   # true OR false -> true
        "true", "and",           # true AND true -> true
        "not"                    # NOT true -> false
    ]
    interpreter.execute(commands)
    assert interpreter.stack == [False]

def test_integration_array_operations(interpreter):
    commands = [
        "[1,2,3,4,5]", "1", "3", "getinterval", # Get 2nd to 4th elements
        "0", "get"                              # Get 1st element
    ]
    interpreter.execute(commands)
    assert interpreter.stack == [2]

def test_integration_print(interpreter, capsys):
    interpreter.execute(["10", "print"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "10"

def test_integration_string_operations(interpreter):
    commands = [
        "Hello world",     # Push a string
        "length",             # Get the length of the string
    ]
    interpreter.execute(commands)
    assert interpreter.stack == [11]
