import pytest # type: ignore
from main import PostScriptInterpreter  

@pytest.fixture
def interpreter():
    return PostScriptInterpreter()

@pytest.fixture
def interpreter_lexical():
    return PostScriptInterpreter(use_lexical_scoping=True)

def test_push_number(interpreter):
    interpreter.execute("42")
    assert interpreter.stack == [42]

def test_push_negative_number(interpreter):
    interpreter.execute("-42")
    assert interpreter.stack == [-42]

def test_exch(interpreter):
    interpreter.execute(["1", "2", "exch"])
    assert interpreter.stack == [2, 1]

def test_pop(interpreter):
    interpreter.execute(["1", "2", "pop"])
    assert interpreter.stack == [1]

def test_copy(interpreter):
    interpreter.execute(["1", "2", "3", "2", "copy"])
    assert interpreter.stack == [1, 2, 3, 2, 3]

def test_dup(interpreter):
    interpreter.execute(["1", "dup"])
    assert interpreter.stack == [1, 1]

def test_clear(interpreter):
    interpreter.execute(["1", "2", "3", "clear"])
    assert interpreter.stack == []

def test_count(interpreter):
    interpreter.execute(["1", "2", "3", "count"])
    assert interpreter.stack == [1, 2, 3, 3]

def test_add(interpreter):
    interpreter.execute(["1", "2", "add"])
    assert interpreter.stack == [3]

def test_sub(interpreter):
    interpreter.execute(["3", "1", "sub"])
    assert interpreter.stack == [2]

def test_mul(interpreter):
    interpreter.execute(["3", "2", "mul"])
    assert interpreter.stack == [6]

def test_div(interpreter):
    interpreter.execute(["6", "3", "div"])
    assert interpreter.stack == [2.0]

def test_idiv(interpreter):
    interpreter.execute(["7", "3", "idiv"])
    assert interpreter.stack == [2]

def test_mod(interpreter):
    interpreter.execute(["7", "3", "mod"])
    assert interpreter.stack == [1]

def test_abs(interpreter):
    interpreter.execute(["-7", "abs"])
    assert interpreter.stack == [7]

def test_neg(interpreter):
    interpreter.execute(["7", "neg"])
    assert interpreter.stack == [-7]

def test_ceiling(interpreter):
    interpreter.execute(["7.1", "ceiling"])
    assert interpreter.stack == [8]

def test_floor(interpreter):
    interpreter.execute(["7.9", "floor"])
    assert interpreter.stack == [7]

def test_round(interpreter):
    interpreter.execute(["7.6", "round"])
    assert interpreter.stack == [8]

def test_sqrt(interpreter):
    interpreter.execute(["9", "sqrt"])
    assert interpreter.stack == [3.0]

def test_dict(interpreter):
    interpreter.execute(["dict"])
    assert interpreter.stack == [{}]

def test_length(interpreter):
    interpreter.execute(["1", "2", "3", "length"])
    assert interpreter.stack == [3]

def test_def_and_lookup_dynamic():
    interpreter = PostScriptInterpreter(use_lexical_scoping=False)
    interpreter.execute(["/x", "10", "def", "x"])
    assert interpreter.stack == [10]

def test_def_and_lookup_lexical(interpreter_lexical):
    interpreter_lexical.execute(["/x", "10", "def", "x"])
    assert interpreter_lexical.stack == [10]

def test_eq(interpreter):
    interpreter.execute(["10", "10", "eq"])
    assert interpreter.stack == [True]

def test_ne(interpreter):
    interpreter.execute(["10", "20", "ne"])
    assert interpreter.stack == [True]

def test_gt(interpreter):
    interpreter.execute(["20", "10", "gt"])
    assert interpreter.stack == [True]

def test_lt(interpreter):
    interpreter.execute(["10", "20", "lt"])
    assert interpreter.stack == [True]

def test_and(interpreter):
    interpreter.execute(["True", "False", "and"])
    assert interpreter.stack == [False]

def test_or(interpreter):
    interpreter.execute(["True", "False", "or"])
    assert interpreter.stack == [True]

def test_not(interpreter):
    interpreter.execute(["False", "not"])
    assert interpreter.stack == [True]

def test_true_false(interpreter):
    interpreter.execute(["True", "False"])
    assert interpreter.stack == [True, False]

def test_print(interpreter, capsys):
    interpreter.execute(["10", "print"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "10"
