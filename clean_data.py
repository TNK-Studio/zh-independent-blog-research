import os
import json
from utils import PASS_DOMAIN


class Cleaner:
    def __init__(self, path):
        self.path = path
        self.all_sites = iter(os.listdir(path))

    def clear_pass_domain_data(self):
        for i in self.all_sites:
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
            json.dump(data,f)


if __name__ == "__main__":
    c = Cleaner('data')
    c.clear_pass_domain_data()
    c.clean_run_status()
