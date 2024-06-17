# tests/test_my_function.py
from my_module.my_function_code import add

def test_add_positive_numbers():
    assert add(1, 2) == 3, "Should be 3"

def test_add_negative_numbers():
    assert add(-1, -2) == -3, "Should be -3"

def test_add_zero():
    assert add(0, 0) == 0, "Should be 0"

def test_add_positive_and_negative():
    assert add(1, -1) == 0, "Should be 0"

def test_add_large_numbers():
    assert add(1e6, 1e6) == 2e6, "Should be 2000000"

