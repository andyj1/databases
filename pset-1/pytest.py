#test_sample.py
import pytest

def f():
    raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):
        f()

def func(x):
    return x+1

def test_func():
    assert func(3) == 4

class TestClass:
    def test_one(self):
        x = "this"
        assert "this" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")