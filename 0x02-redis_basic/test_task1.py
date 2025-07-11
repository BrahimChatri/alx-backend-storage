#!/usr/bin/env python3
"""
Test file for Task 1 - Reading from Redis and recovering original type
"""
Cache = __import__('exercise').Cache

cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn) == value
print("Task 1 tests passed.")
