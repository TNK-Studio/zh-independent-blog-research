import json
import os
import asyncio
import sys

from urllib.parse import urljoin
from urllib.parse import urlparse
from queue import Queue
from get import get_data
from itertools import chain

from schema import SiteInfoItem


def app(count, batch_size):
    q = Queue()

    # init queue with last run-status
    with open('run_status.json', 'r') as f:
        last_run_status = json.load(f)
        list(map(q.put, last_run_status['q']))

    if not os.path.exists('data'):
        os.mkdir('data')
    visited_sites = set([site[:-5] for site in os.listdir('data')])

    while not q.empty() and count > 0:
        try:
            urls = [q.get() for i in range(batch_size) if not q.empty()]
            print(urls)
            r = get_data(urls)
            # update visited site
            list(map(visited_sites.add, [
                 urlparse(url).netloc for url in urls]))
            all_friend_links = list(chain(*[site.friends for site in r]))

            # if site has been visited, do not put in queue
            link_need_to_put_in_q = [link for link in all_friend_links if urlparse(
                link).netloc not in visited_sites]
            list(map(q.put, link_need_to_put_in_q))
            count -= batch_size
            print(count, q.qsize())
        except Exception as e:
            with open("run_status.json", 'w') as f:
                json.dump({
                    "q": list(q.queue)
                }, f)
            print(e)
            print("exit by error")
            break
    else:
        with open("run_status.json", 'w') as f:
            json.dump({
                "q": list(q.queue)
            }, f)


if __name__ == "__main__":
    app(8, 8)
