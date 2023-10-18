#!/usr/bin/env python3
"""
Web file
"""
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            store.incr("count:" + url)
            return cached_data.decode("utf-8")

        html = method(url)

        store.incr("count:" + url)
        store.setex(cached_key, 10, html)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    res = requests.get(url)
    return res.text


if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'
    print(get_page(url))
