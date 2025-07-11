#!/usr/bin/env python3
"""
Alternative web cache implementation without decorators
This is for comparison to show how decorators simplify the code
"""
import redis
import requests


# Global Redis client
redis_client = redis.Redis()


def get_page_no_decorator(url: str) -> str:
    """
    Get the HTML content of a URL and cache it (without using decorators).
    
    The function tracks how many times a particular URL was accessed
    in the key "count:{url}" and caches the result with an expiration
    time of 10 seconds.
    
    Args:
        url: The URL to fetch
        
    Returns:
        The HTML content of the URL
    """
    # Cache key for page content
    page_key = f"cached:{url}"
    count_key = f"count:{url}"
    
    # Always increment the count for each access
    redis_client.incr(count_key)
    
    # Check if page is cached
    cached_page = redis_client.get(page_key)
    if cached_page:
        print(f"Cache hit for {url}")
        return cached_page.decode('utf-8')
    
    # Cache miss - fetch the page
    print(f"Cache miss for {url} - fetching from web")
    
    # Use requests to get the HTML content
    response = requests.get(url)
    content = response.text
    
    # Cache the page content with an expiration of 10 seconds
    redis_client.setex(page_key, 10, content)
    
    return content


def get_url_count_alt(url: str) -> int:
    """
    Get the access count for a URL.
    
    Args:
        url: The URL to check
        
    Returns:
        The number of times the URL has been accessed
    """
    count_key = f"count:{url}"
    count = redis_client.get(count_key)
    return int(count) if count else 0


if __name__ == "__main__":
    # Example usage
    print("Alternative implementation (without decorators)")
    print("=" * 50)
    
    url = "http://httpbin.org/html"
    
    print(f"1. First request to {url}")
    content1 = get_page_no_decorator(url)
    print(f"Content length: {len(content1)}")
    print(f"Access count: {get_url_count_alt(url)}")
    
    print(f"\n2. Second request to {url}")
    content2 = get_page_no_decorator(url)
    print(f"Content length: {len(content2)}")
    print(f"Access count: {get_url_count_alt(url)}")
    print(f"Same content: {content1 == content2}")
