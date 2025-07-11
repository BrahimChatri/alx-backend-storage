#!/usr/bin/env python3
"""
Test file for web cache functionality
"""
import time
from web import get_page, get_url_count

def test_web_cache():
    """Test the web cache functionality"""
    
    # Use a slow test URL
    slow_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    fast_url = "http://httpbin.org/delay/1"
    
    print("Testing web cache and URL tracking...")
    print("=" * 50)
    
    # Test with slow URL
    print(f"\n1. First request to slow URL (should be slow)")
    start_time = time.time()
    content1 = get_page(slow_url)
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    print(f"Content length: {len(content1)} characters")
    print(f"URL access count: {get_url_count(slow_url)}")
    
    print(f"\n2. Second request to same URL (should be cached and fast)")
    start_time = time.time()
    content2 = get_page(slow_url)
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    print(f"Content length: {len(content2)} characters")
    print(f"URL access count: {get_url_count(slow_url)}")
    print(f"Content matches: {content1 == content2}")
    
    print(f"\n3. Third request to same URL (should still be cached)")
    start_time = time.time()
    content3 = get_page(slow_url)
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    print(f"URL access count: {get_url_count(slow_url)}")
    
    print(f"\n4. Waiting for cache to expire (10+ seconds)...")
    time.sleep(11)
    
    print(f"\n5. Request after cache expiration (should be slow again)")
    start_time = time.time()
    content4 = get_page(slow_url)
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    print(f"URL access count: {get_url_count(slow_url)}")
    
    # Test with different URL
    print(f"\n6. Testing different URL")
    start_time = time.time()
    content5 = get_page(fast_url)
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    print(f"Content length: {len(content5)} characters")
    print(f"URL access count for fast_url: {get_url_count(fast_url)}")
    print(f"URL access count for slow_url: {get_url_count(slow_url)}")

if __name__ == "__main__":
    test_web_cache()
