import math

from calc_utils import add, is_palindrome, factorial


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("A man a plan a canal Panama") is True
    assert is_palindrome("hello") is False


def test_factorial():
    assert factorial(0) == 1
    assert factorial(5) == 120
    # TODO: add a test case for factorial with negative input


def test_factorial_large_n_does_not_hit_recursion_limit():
    # factorial(2000) exceeds Python's default recursion limit (1000) if
    # implemented via naive recursion; it must still return the correct
    # value without raising RecursionError.
    result = factorial(2000)
    assert result == math.factorial(2000)
