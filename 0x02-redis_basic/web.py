#!/usr/bin/env python3
"""
Web cache and URL tracker using Redis
"""
import redis
import requests
from typing import Callable
from functools import wraps


# Global Redis client
redis_client = redis.Redis()


def cache_page(call: Callable) -> Callable:
    """
    Decorator to cache a web page and track access count
    
    Args:
        call: The function to be decorated
        
    Returns:
        The decorated function with caching and tracking
    """
    @wraps(call)
    def wrapper(url: str) -> str:
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
        response = call(url)
        
        # Cache the page content with an expiration of 10 seconds
        redis_client.setex(page_key, 10, response)
        
        return response
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL and cache it.
    
    The function tracks how many times a particular URL was accessed
    in the key "count:{url}" and caches the result with an expiration
    time of 10 seconds.
    
    Args:
        url: The URL to fetch
        
    Returns:
        The HTML content of the URL
    """
    # Use requests to get the HTML content
    response = requests.get(url)
    return response.text


def get_url_count(url: str) -> int:
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

