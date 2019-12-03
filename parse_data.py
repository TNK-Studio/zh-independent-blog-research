
import json
import os
from dataclasses import dataclass
from requests_html import HTML

from get import SiteFeatureTransformer
from schema import SiteInfoItem


@dataclass
class HTMLRes():
    html: HTML
    url: str = ''


def recovery_data():
    """
    """
    with open('site/src/data.json', 'r') as f:
        all_site = json.load(f)
        for site in all_site:
            site = SiteInfoItem(**site)
            with open(f'data/{site.domain}.json', 'w') as f:
                site.save_to_file(f)


def parse_data():
    """
    添加新的考察特征时，从缓存的 html 中获取数据，更新到站点数据中。
    """
    for itemdir in iter(os.listdir('data')):
        try:
            site_path = 'data/'+itemdir
            with open(site_path, 'r') as f:
                item = {}
                try:
                    item = json.load(f)
                except Exception as e:
                    print(e)
                domain = itemdir[:-5]
                html_path = f'html/{domain}.html'
            if os.path.exists(html_path):
                with open(html_path, 'r') as fhtml:
                    url = item['url']
                    html = HTML(url=url, html=fhtml.read())
                    site_feature = SiteFeatureTransformer(
                        url=url, r=HTMLRes(url=url, html=html), friends=item['friends'])
                    site = SiteInfoItem(**site_feature.to_data())

                with open(site_path, 'w') as f:
                    site.save_to_file(f)
            else:
                print(f'{domain} 的缓存 html 文件不存在')

        except Exception as e:
            print(e)
            print(f"打开 {itemdir} 失败")


if __name__ == "__main__":
    # recovery_data()
    parse_data()