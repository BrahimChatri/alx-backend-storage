#!/usr/bin/env python3
"""
Example usage of the web cache functionality
"""

# Example of how to use the web cache
def example_usage():
    """
    Example demonstrating the web cache functionality
    
    Note: This requires Redis server to be running
    """
    
    from web import get_page, get_url_count
    
    # Example URLs
    url1 = "http://www.google.com"
    url2 = "http://slowwly.robertomurray.co.uk/delay/2000/url/http://www.example.com"
    
    print("Web Cache Example Usage")
    print("=" * 30)
    
    print("\n1. First request (cache miss):")
    content1 = get_page(url1)
    print(f"Content length: {len(content1)}")
    print(f"Access count: {get_url_count(url1)}")
    
    print("\n2. Second request (cache hit):")
    content2 = get_page(url1)
    print(f"Content length: {len(content2)}")
    print(f"Access count: {get_url_count(url1)}")
    print(f"Same content: {content1 == content2}")
    
    print("\n3. Different URL:")
    content3 = get_page(url2)
    print(f"Content length: {len(content3)}")
    print(f"Access count for url1: {get_url_count(url1)}")
    print(f"Access count for url2: {get_url_count(url2)}")


if __name__ == "__main__":
    print("This example requires Redis server to be running.")
    print("Run: redis-server")
    print("Then execute this script.")
    # Uncomment the line below to run the example
    # example_usage()
