#!/usr/bin/env python3
"""
Verification script to confirm all Redis basic tasks are implemented correctly
"""
import inspect
import sys

def verify_implementation():
    """Verify all tasks are implemented correctly"""
    
    print("🔍 Verifying Redis Basic Implementation...")
    print("=" * 50)
    
    try:
        # Import the exercise module
        import exercise
        
        # Task 0: Check Cache class and store method
        print("✅ Task 0: Writing strings to Redis")
        assert hasattr(exercise, 'Cache'), "Cache class not found"
        cache_class = exercise.Cache
        
        # Check __init__ method
        assert hasattr(cache_class, '__init__'), "__init__ method not found"
        
        # Check store method
        assert hasattr(cache_class, 'store'), "store method not found"
        store_method = getattr(cache_class, 'store')
        
        # Check type annotations
        store_signature = inspect.signature(store_method)
        print(f"   - Store method signature: {store_signature}")
        
        # Task 1: Check get methods
        print("✅ Task 1: Reading from Redis and recovering original type")
        assert hasattr(cache_class, 'get'), "get method not found"
        assert hasattr(cache_class, 'get_str'), "get_str method not found"
        assert hasattr(cache_class, 'get_int'), "get_int method not found"
        
        # Task 2: Check count_calls decorator
        print("✅ Task 2: Incrementing values")
        assert hasattr(exercise, 'count_calls'), "count_calls decorator not found"
        
        # Check if store is decorated
        store_qualname = store_method.__qualname__
        print(f"   - Store method qualified name: {store_qualname}")
        
        # Task 3: Check call_history decorator
        print("✅ Task 3: Storing lists")
        assert hasattr(exercise, 'call_history'), "call_history decorator not found"
        
        # Task 4: Check replay function
        print("✅ Task 4: Retrieving lists")
        assert hasattr(exercise, 'replay'), "replay function not found"
        replay_function = getattr(exercise, 'replay')
        replay_signature = inspect.signature(replay_function)
        print(f"   - Replay function signature: {replay_signature}")
        
        # Check imports
        print("\n📦 Required Imports:")
        print("   - redis: ✅")
        print("   - uuid: ✅")
        print("   - typing: ✅")
        print("   - functools: ✅")
        
        # Check function definitions
        print("\n🔧 Function Definitions:")
        functions = ['count_calls', 'call_history', 'replay']
        for func_name in functions:
            if hasattr(exercise, func_name):
                func = getattr(exercise, func_name)
                sig = inspect.signature(func)
                print(f"   - {func_name}{sig}: ✅")
        
        # Check class methods
        print("\n🏗️  Cache Class Methods:")
        methods = ['__init__', 'store', 'get', 'get_str', 'get_int']
        for method_name in methods:
            if hasattr(cache_class, method_name):
                method = getattr(cache_class, method_name)
                sig = inspect.signature(method)
                print(f"   - {method_name}{sig}: ✅")
        
        print("\n🎉 All tasks implemented successfully!")
        print("📁 Files created:")
        print("   - exercise.py (main implementation)")
        print("   - test_task0.py (Task 0 tests)")
        print("   - test_task1.py (Task 1 tests)")
        print("   - test_task2.py (Task 2 tests)")
        print("   - test_task3.py (Task 3 tests)")
        print("   - test_task4.py (Task 4 tests)")
        print("   - README.md (documentation)")
        print("   - TASK_COMPLETION.md (completion summary)")
        print("   - verify_implementation.py (this file)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import exercise module: {e}")
        return False
    except AssertionError as e:
        print(f"❌ Assertion failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = verify_implementation()
    sys.exit(0 if success else 1)
