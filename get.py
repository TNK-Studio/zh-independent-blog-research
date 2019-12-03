"""
抓取&处理数据
"""

import os
import requests
import re

from dataclasses import dataclass
from urllib.parse import urljoin
from urllib.parse import urlparse
from requests_html import AsyncHTMLSession
# from requests_html import HTMLSession
from utils import PASS_DOMAIN, geuss_link_url, rm_slash, has_url_html_been_fetched
from itertools import chain
from schema import SiteInfoItem
from site_feature import SiteFeatureTransformer

from is_site_a_zh_i9t_blog import test


asession = AsyncHTMLSession()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
asession.mount('http://', adapter)
asession.mount('https://', adapter)


# 标题中出现这些关键词时，基本上不会是个人博客
BLACK_WORDS = set({
    "SEO", "官方", "导航", "网址"
})


def save_html(domain, html):
    path = os.path.join('html', f'{domain}.html')
    with open(path, 'w') as f:
        f.write(html)


def get_data(urls):
    res = get_frineds_and_res(urls)
    data = []
    for url, friends, r in res:
        site_feature = SiteFeatureTransformer(r=r, url=url, friends=friends)
        if site_feature.feature['has_zh_text'] and test(site_feature.feature):
            site = SiteInfoItem(**site_feature.to_data())
            site_path = f'data/{site.domain}.json'
            with open(site_path, 'w') as f:
                site.save_to_file(f)
            save_html(site.domain, str(r.html.html))
            data.append(site)
        else:
            print('{} maybe not personal zh blog'.format(url))
    return data


def get_url_html(url):
    async def f():
        # print("get:{}".format(url))
        try:
            r = await asession.get(url, timeout=10)
            return r
        except requests.exceptions.ConnectTimeout:
            # print("{} 链接超时，不可访问".format(url))
            pass
        except:
            pass
            # print("{} 链接错误，不可访问".format(url))
    return f


def get_frineds_and_res(urls):
    """
    找到给定 url 的友情链接列表,返回友链 & 友链页面 html
    """
    urls = [url for url in urls if not has_url_html_been_fetched(url)]
    all_urls = list(chain(*[geuss_link_url(url) for url in urls]))
    res = []
    try:
        results = asession.run(*[get_url_html(url)
                                 for url in all_urls])

        for url in urls:
            friends = []
            index_rhtml = None
            for r in results:
                if r:
                    if friends and index_rhtml:
                        break
                    elif r.status_code == 200 and urlparse(r.url).netloc == urlparse(url).netloc:
                        if not friends:
                            pass_domain = PASS_DOMAIN + \
                                [urlparse(r.url).netloc]
                            friends = list(
                                map(lambda url: rm_slash(url), r.html.absolute_links))

                            friends = list(filter(lambda url: all([url.find(
                                pdomain) == -1 for pdomain in pass_domain]) & (urlparse(url).path == ""), set(friends)))
                        if not index_rhtml and rm_slash(r.url) == url:
                            index_rhtml = r
                else:
                    pass
            if friends and index_rhtml:
                res.append((url, friends, index_rhtml))
    except Exception as e:
        print(e)
    finally:
        return res


if __name__ == "__main__":
    urls = ["https://www.magicican.com",
            "https://elfgzp.cn",
            "https://ruterly.com",
            "https://www.tsuna.moe"]
    data = {
        "has_archive": 0,
        "has_tag": 1,
        "has_category": 0,
        "has_about": 1,
        "has_theme": 1,
        "has_zh_text": 1,
        "has_blog_text": 1,
        "has_generator": 1,
        "has_rss": 1,
        "len_friends": 1
        # "tld": "com",
        # "sld": "1a23"
    }

    print(test(data))
    # get_data(urls)
