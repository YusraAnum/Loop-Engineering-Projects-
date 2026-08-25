def add(a, b):
    return a + b


# TODO: is_palindrome does not validate that s is actually a string
def is_palindrome(s):
    s = "".join(ch.lower() for ch in s if ch.isalnum())
    return s == s[::-1]


def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
