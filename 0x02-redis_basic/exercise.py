#!/usr/bin/env python3
"""
storing strings in Redis
"""


import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps
import requests


def count_calls(method: Callable) -> Callable:
    """Counts how many times methods of the Cache class are called."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwds)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Stores the history of inputs and outputs for a particular function.

    Everytime the original function will be called,
    we will add its input parameters to one list in redis,
    and store its output into another list.

    Use the decorated function’s qualified name and append ":inputs"
    and ":outputs" to create input and output list keys, respectively.

    In the new function that the decorator will return,
    use rpush to append the input arguments.
    Remember that Redis can only store strings, bytes and numbers.
    Therefore, we can simply use str(args) to normalize.
    We can ignore potential kwargs for now.

    Execute the wrapped function to retrieve the output.
    Store the output using rpush in the "...:outputs" list,
    then return the output.
    """

    @wraps(method)
    def wrapper(self, *args):
        """Wrapper function"""
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        output = method(self, *args)
        self._redis.rpush(method.__qualname__ + ":outputs", str(output))
        return output

    return wrapper


def replay(method: Callable):
    """Display the history of calls of a particular function."""
    r = redis.Redis()
    key = method.__qualname__
    inputs = r.lrange(key + ":inputs", 0, -1)
    outputs = r.lrange(key + ":outputs", 0, -1)
    print("{} was called {} times:".format(key, r.get(key).decode("utf-8")))
    for i in range(len(inputs)):
        print("{}(*{}) -> {}".format(key, inputs[i].decode("utf-8"),
                                     outputs[i].decode("utf-8")))


def get_page(url: str) -> str:
    """
    Return the HTML content of a particular URL
    """
    r = requests.get(url)
    return r.text


class Cache:
    """
    A simple chache class using Redis.

    In the __init__ method, store an instance of the Redis client as
    a private variable named _redis (using redis.Redis())
    and flush the instance using flushdb.

    Create a store method that takes a data argument and returns a string.
    The method should generate a random key (e.g. using uuid),
    store the input data in Redis using the random key and return the key.

    Type-annotate store correctly.
    Remember that data can be a str, bytes, int or float.
    """

    def __init__(self):
        """Initialize the Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in Redis and returns a unique key.

        Args:
            data (Union[str, bytes, int, float]):
            The data to be stored in the cache.

        Returns:
            str: A unique key associated with the stored data.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str,
                                                                    bytes,
                                                                    int,
                                                                    float]:
        """
        Retrieves data from Redis based on the provided key.

        Args:
            key (str): The key associated with the data in the cache.
            fn (Callable, optional): A callable function to convert
            the data back to the desired format.

        Returns:
            Union[str, bytes, int, None]: The retrieved data or None
            if the key does not exist.
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string from Redis based on the provided key.

        Args:
            key (str): The key associated with the string in the cache.

        Returns:
            Union[str, None]: The retrieved string or None
            if the key does not exist.
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer from Redis based on the provided key.

        Args:
            key (str): The key associated with the integer in the cache.

        Returns:
            Union[int, None]: The retrieved integer or None
            if the key does not exist.
        """
        return self.get(key, int)
