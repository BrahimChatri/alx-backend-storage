# 0x02-redis_basic

This directory contains the implementation of Redis basic operations using Python with Redis client library.

## Task Descriptions

### Task 0: Writing strings to Redis
- **File**: `exercise.py`
- **Description**: Create a Cache class with `__init__` method that stores a Redis client instance and flushes the database. Implement a `store` method that generates a random key, stores data in Redis, and returns the key.
- **Requirements**:
  - Store Redis client as private variable `_redis`
  - Use `flushdb()` to clear database
  - Generate random key using `uuid`
  - Type-annotate the `store` method
  - Data can be `str`, `bytes`, `int`, or `float`

### Task 1: Reading from Redis and recovering original type
- **File**: `exercise.py`
- **Description**: Implement a `get` method that retrieves data and optionally converts it using a callable function. Also implement `get_str` and `get_int` helper methods.
- **Requirements**:
  - `get` method takes key and optional callable
  - Preserve original Redis.get behavior for non-existent keys
  - `get_str` automatically converts to string
  - `get_int` automatically converts to integer

### Task 2: Incrementing values
- **File**: `exercise.py`
- **Description**: Implement a `count_calls` decorator that counts how many times methods are called using Redis INCR command.
- **Requirements**:
  - Decorator takes a Callable and returns a Callable
  - Use method's `__qualname__` as the key
  - Increment counter each time method is called
  - Use `functools.wraps` to preserve function metadata
  - Decorate `Cache.store` with `count_calls`

### Task 3: Storing lists
- **File**: `exercise.py`
- **Description**: Implement a `call_history` decorator that stores input parameters and outputs in Redis lists using RPUSH.
- **Requirements**:
  - Store inputs in `{qualname}:inputs` list
  - Store outputs in `{qualname}:outputs` list
  - Use `str(args)` to normalize input arguments
  - Use RPUSH to append to lists
  - Decorate `Cache.store` with `call_history`

### Task 4: Retrieving lists
- **File**: `exercise.py`
- **Description**: Implement a `replay` function that displays the history of calls for a particular function.
- **Requirements**:
  - Use LRANGE to retrieve inputs and outputs
  - Display format: `{qualname} was called N times:`
  - Show each call: `{qualname}(*{input}) -> {output}`
  - Use `zip` to iterate over inputs and outputs

## Implementation Details

### Cache Class
```python
class Cache:
    def __init__(self):
        # Initialize Redis client and flush database
        
    def store(self, data: Union[str, bytes, int, float]) -> str:
        # Store data with random UUID key
        
    def get(self, key: str, fn: Optional[Callable] = None):
        # Retrieve data with optional conversion
        
    def get_str(self, key: str) -> Optional[str]:
        # Get data as string
        
    def get_int(self, key: str) -> Optional[int]:
        # Get data as integer
```

### Decorators
```python
def count_calls(method: Callable) -> Callable:
    # Count method calls using Redis INCR
    
def call_history(method: Callable) -> Callable:
    # Store input/output history using Redis lists
```

### Utility Functions
```python
def replay(method: Callable) -> None:
    # Display call history for a method
```

## Features Implemented

1. **Redis Integration**: Full Redis client integration with connection handling
2. **Type Annotations**: Complete type annotations for all methods
3. **UUID Key Generation**: Random key generation for data storage
4. **Data Type Conversion**: Flexible data retrieval with optional conversion
5. **Call Counting**: Automatic method call counting with decorators
6. **History Tracking**: Input/output history storage and retrieval
7. **Error Handling**: Proper handling of non-existent keys
8. **Decorator Composition**: Multiple decorators on the same method

## Usage Examples

### Basic Storage and Retrieval
```python
cache = Cache()

# Store different data types
key1 = cache.store("hello")
key2 = cache.store(b"world")
key3 = cache.store(42)
key4 = cache.store(3.14)

# Retrieve with conversion
text = cache.get_str(key1)  # "hello"
number = cache.get_int(key3)  # 42
```

### Call Counting
```python
cache = Cache()
cache.store("test1")
cache.store("test2")
cache.store("test3")

# Check how many times store was called
count = cache.get(cache.store.__qualname__)  # b'3'
```

### History Replay
```python
cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)

# Display call history
replay(cache.store)
# Output:
# Cache.store was called 3 times:
# Cache.store(*('foo',)) -> uuid-key-1
# Cache.store(*('bar',)) -> uuid-key-2
# Cache.store(*(42,)) -> uuid-key-3
```

## Dependencies

- `redis`: Redis Python client library
- `uuid`: UUID generation (built-in)
- `typing`: Type annotations (built-in)
- `functools`: Decorator utilities (built-in)

## Installation

1. Install Redis server
2. Install Python Redis client: `pip install redis`
3. Ensure Redis server is running on localhost:6379

## Testing

Run the test files to verify implementation:
```bash
python3 test_task0.py  # Test basic storage
python3 test_task1.py  # Test data retrieval
python3 test_task2.py  # Test call counting
python3 test_task3.py  # Test history storage
python3 test_task4.py  # Test history replay
```

## Repository Information

- **Repository**: alx-backend-storage
- **Directory**: 0x02-redis_basic
- **File**: exercise.py
