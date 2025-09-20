"""Fibonacci utilities.

This module provides a simple, efficient implementation of the Fibonacci
sequence and a tiny smoke-test when run as a script.

The function `fibonacci(n)` returns the n-th Fibonacci number using a
0-based index so:
  fibonacci(0) == 0
  fibonacci(1) == 1

The implementation is iterative (O(n) time, O(1) memory) and performs
basic input validation.
"""

from __future__ import annotations

def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number (0-based).

    Args:
        n: A non-negative integer index.

    Returns:
        The n-th Fibonacci number as an int.

    Raises:
        TypeError: If n is not an int.
        ValueError: If n is negative.
    """

    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")

    # Fast paths
    if n == 0:
        return 0
    if n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    # Simple smoke tests
    tests = {
        0: 0,
        1: 1,
        2: 1,
        3: 2,
        5: 5,
        10: 55,
        20: 6765,
    }

    for k, expected in tests.items():
        got = fibonacci(k)
        print(f"fibonacci({k}) = {got}")
        assert got == expected, f"expected {expected} for n={k}, got {got}"

    print("All smoke tests passed.")
