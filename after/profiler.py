"""Computational tasks for Lab 9 profiling."""
import time


def slow_function():
    time.sleep(2)
    total = 0
    for i in range(10000):
        total += i ** 2
    return total


def fast_function():
    total = 0
    for i in range(100):
        total += i ** 2
    return total


def memory_intensive_function():
    total = 0
    for i in range(10000000):
        total += i ** 2
    return total


def optimized_fast_function():
    """Sum the same squares with the exact closed form, using integer arithmetic."""
    n = 100
    return n * (n - 1) * (2 * n - 1) // 6


def main():
    slow_function()
    optimized_fast_function()
    memory_intensive_function()


if __name__ == "__main__":
    main()
