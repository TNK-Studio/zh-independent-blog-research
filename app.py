import os
import json
import time
from task import task
from multiprocessing import cpu_count, Pool, Manager, Queue, TimeoutError
# from bloom_filter import BloomFilter
from urllib.parse import urlparse

# bloom = BloomFilter(max_elements=1000000, error_rate=0.1)
# some bug in bloom


def app(unlimit=False):
    if not os.path.exists('data'):
        os.mkdir('data')

    bloom = set()
    list(map(bloom.add, [site[:-5] for site in os.listdir('data')]))

    manager = Manager()
    q = manager.Queue()
    print(q.qsize())
    # 初始化的对列
    with open('run_status.json', 'r') as f:
        last_run_status = json.load(f)
        list(map(q.put, last_run_status['q']))

    print(q.qsize())
    try:
        while not q.empty():
            with Pool(cpu_count()) as pool:
                ress = [pool.apply_async(task, (q, bloom, 8))
                        for _ in range(cpu_count()//2)]
                for res in ress:
                    try:
                        pid, new_links = res.get(timeout=100)
                        link_need_to_put_in_q = [link for link in new_links if urlparse(
                            link).netloc not in bloom]
                        print(f'{pid} 完成了一批任务')
                        if unlimit:
                            list(map(q.put, link_need_to_put_in_q))
                            print(f'新链接加入队列：{link_need_to_put_in_q}')
                        print(q.qsize())
                    except Exception as e:
                        print("some task error")
                        # fixme
                        print(e)

    except Exception as e:
        print(e)
        with open('run_status.json', 'r') as f:
            r = []
            while not q.empty():
                r.append(q.get())
            json.dump({
                'q': r
            }, f)
        pass


if __name__ == "__main__":
    start = time.time()
    print(start)
    app(unlimit=True)
    end = time.time()
    print(end)
    print(end-start)
