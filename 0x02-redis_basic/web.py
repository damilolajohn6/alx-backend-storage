#!/usr/bin/env python3

"""
create a web cache
"""

import requests
import time
from functools import wraps

CACHE_EXPIRATION = 10  # seconds
url_access_counts = {}  # Track URL access counts

def cache_result(url):
    def decorator_get_page(func):
        cache = {}

        @wraps(func)
        def wrapper(url):
            if url in cache and time.time() - cache[url]['timestamp'] < CACHE_EXPIRATION:
                return cache[url]['content']

            content = func(url)

            # Update cache
            cache[url] = {'content': content, 'timestamp': time.time()}
            return content

        return wrapper

    return decorator_get_page

@cache_result(url_access_counts)
def get_page(url: str) -> str:
    global url_access_counts
    if url in url_access_counts:
        url_access_counts[url] += 1
    else:
        url_access_counts[url] = 1

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Test the get_page function
if __name__ == "__main__":
    slow_url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.google.com"
    fast_url = "https://www.example.com"

    # Access the slow URL multiple times to trigger caching
    for i in range(3):
        print(f"Accessing slow URL ({slow_url})...")
        slow_content = get_page(slow_url)
        print(f"Content (slow): {slow_content}")

    # Access the fast URL
    print(f"Accessing fast URL ({fast_url})...")
    fast_content = get_page(fast_url)
    print(f"Content (fast): {fast_content}")

    # Wait for cache expiration (11 seconds) and access slow URL again
    time.sleep(11)
    print("Cache expired. Accessing slow URL again...")
    slow_content_cached = get_page(slow_url)
    print(f"Content (slow, cached): {slow_content_cached}")

    # Display URL access counts
    print("URL access counts:")
    for url, count in url_access_counts.items():
        print(f"{url}: {count}")
