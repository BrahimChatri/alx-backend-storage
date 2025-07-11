#!/usr/bin/env python3
"""
Test file for Task 4 - Retrieving lists
"""
Cache = __import__('exercise').Cache
replay = __import__('exercise').replay

cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)
