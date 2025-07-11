#!/usr/bin/env python3
"""
Redis Cache implementation with decorators for counting and history tracking
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.
    
    Args:
        method: The method to be decorated
        
    Returns:
        The decorated method that increments a counter
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the count for the method
        """
        # Use the qualified name as the key
        key = method.__qualname__
        # Increment the count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a function.
    
    Args:
        method: The method to be decorated
        
    Returns:
        The decorated method that stores input/output history
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores inputs and outputs
        """
        # Create keys for inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        
        # Store input arguments
        self._redis.rpush(input_key, str(args))
        
        # Execute the wrapped function to get output
        output = method(self, *args, **kwargs)
        
        # Store output
        self._redis.rpush(output_key, output)
        
        return output
    return wrapper


class Cache:
    """
    Cache class for Redis operations
    """
    
    def __init__(self):
        """
        Initialize the Cache instance with Redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key.
        
        Args:
            data: The data to store (str, bytes, int, or float)
            
        Returns:
            The random key used to store the data
        """
        # Generate a random key
        key = str(uuid.uuid4())
        
        # Store the data in Redis
        self._redis.set(key, data)
        
        return key
    
    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Get data from Redis and optionally convert it using a callable.
        
        Args:
            key: The key to retrieve from Redis
            fn: Optional callable to convert the data
            
        Returns:
            The data from Redis, optionally converted
        """
        # Get the data from Redis
        data = self._redis.get(key)
        
        # If data doesn't exist, return None
        if data is None:
            return None
        
        # If a conversion function is provided, use it
        if fn is not None:
            return fn(data)
        
        return data
    
    def get_str(self, key: str) -> Optional[str]:
        """
        Get data from Redis and convert it to a string.
        
        Args:
            key: The key to retrieve from Redis
            
        Returns:
            The data as a string, or None if key doesn't exist
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))
    
    def get_int(self, key: str) -> Optional[int]:
        """
        Get data from Redis and convert it to an integer.
        
        Args:
            key: The key to retrieve from Redis
            
        Returns:
            The data as an integer, or None if key doesn't exist
        """
        return self.get(key, fn=int)


def replay(method: Callable) -> None:
    """
    Display the history of calls for a particular function.
    
    Args:
        method: The method to display history for
    """
    # Get the Redis instance from the method's instance
    redis_instance = method.__self__._redis
    
    # Get the qualified name of the method
    method_name = method.__qualname__
    
    # Get the count of calls
    count = redis_instance.get(method_name)
    if count is None:
        count = 0
    else:
        count = int(count)
    
    print(f"{method_name} was called {count} times:")
    
    # Get inputs and outputs
    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)
    
    # Display the history
    for input_data, output_data in zip(inputs, outputs):
        input_str = input_data.decode("utf-8")
        output_str = output_data.decode("utf-8")
        print(f"{method_name}(*{input_str}) -> {output_str}")
