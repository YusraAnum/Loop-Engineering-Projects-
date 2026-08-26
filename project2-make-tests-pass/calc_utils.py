def add(a, b):
    return a + b


def is_palindrome(s):
    if not isinstance(s, str):
        raise TypeError("is_palindrome expects a string")
    s = "".join(ch.lower() for ch in s if ch.isalnum())
    return s == s[::-1]


def factorial(n):
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)
