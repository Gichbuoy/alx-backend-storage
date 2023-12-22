#!/usr/bin/env python3
"""
Implementing get_page() in a new file
"""

import requests
import redis
import time
from functools import wraps
from typing import Callable

# Create a Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def cache_result(expiration_time=10):
    """
    Decorator to cache the result of a function with a specified
    expiration time.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a key based on function name and arguments
            key = f"{func.__name__}:{args}"

            # Check if the result is in the cache
            cached_result = redis_client.get(key)
            if cached_result:
                return cached_result.decode('utf-8')

            # If not in cache, call the original function
            result = func(*args, **kwargs)

            # Store the result in the cache with the specified expiration time
            redis_client.setex(key, expiration_time, result)

            return result
        return wrapper
    return decorator


@cache_result()
def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a URL and caches the result.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    # Simulate a slow response for testing purposes
    response = requests.get(url)
    time.sleep(3)  # Simulating a 3-second delay
    return response.text


# Example usage
url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.google.com"
html_content = get_page(url)
print(html_content)
