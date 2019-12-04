import json
import os
import asyncio
import sys

from urllib.parse import urljoin
from urllib.parse import urlparse
from queue import Queue
from get import get_data
from itertools import chain

# from bloom_filter import BloomFilter


def task(q, bloom, batch_size):
    pid = os.getpid()
    print(f"开启任务线程-{pid}:")
    urls = [q.get() for i in range(batch_size) if not q.empty()]
    urls = [url for url in urls if urlparse(url).netloc not in bloom]
    print(urls)
    r = get_data(urls)
    # update visited site
    list(map(bloom.add, [
        urlparse(url).netloc for url in urls]))
    all_friend_links = list(chain(*[site.friends for site in r]))

    return pid, all_friend_links


if __name__ == "__main__":
    # bloom = BloomFilter(max_elements=100000, error_rate=0.1)
    bloom = set()  # 过滤器中有些bug，目前还是采用集合来去重
    task(Queue(), bloom, 8)
