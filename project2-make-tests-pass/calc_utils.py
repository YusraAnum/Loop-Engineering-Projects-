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
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
