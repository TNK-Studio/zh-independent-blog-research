import os
import json
from utils import PASS_DOMAIN


class Cleaner:
    def __init__(self, path):
        self.path = path
        self.all_sites = os.listdir(path)

    def clear_pass_domain_data(self):
        """
        清理已经爬取的 pass_domain 的站点数据
        """
        for i in iter(self.all_sites):
            if any([i.endswith(f"{domain}.json") for domain in PASS_DOMAIN]):
                os.remove(os.path.join(self.path, i))
                print(f"{i} has been cleaned")
            

    def clean_run_status(self):
        """
        如果 pass_domian 漏掉了某些 domain，后续的队列中可能出现一些需要过滤 domain 的站点。
        为了提高效率，统一在此清理数据，而不是在抓取数据前作判断。
        """
        with open('run_status.json', 'r') as f:
            data = json.load(f)
            url_need_remove = []
            for url in iter(data['q']):
                if any([url.endswith(domain) for domain in PASS_DOMAIN]):
                    url_need_remove.append(url)

            for url in url_need_remove:
                data['q'].remove(url)
                print(f'{url} has been removed')
        with open('run_status.json', 'w') as f:
            json.dump(data, f)

    def fix_q(self):
        """
        修复异常情况导致下队列丢失的问题
        """
        res = []
        visited_site = set()
        for itemdir in iter(self.all_sites):
            try:
                with open('data/'+itemdir, 'r') as f:
                    item = json.load(f)
                    visited_site.add(item['url'])
                    res.extend(item['friends'])
            except Exception:
                print(f"打开 {itemdir} 失败")

        new_q = list(set(res) - visited_site)
        print(f"fix url queue,count :{len(new_q)}")
        with open('run_status.json', 'w') as f:
            json.dump({
                'q': new_q
            }, f)


if __name__ == "__main__":
    c = Cleaner('data')
    c.clear_pass_domain_data()
    c.fix_q()
    c.clean_run_status()
