"""
抓取数据
"""

import os
import requests
import re

from dataclasses import dataclass
from urllib.parse import urljoin
from urllib.parse import urlparse
from requests_html import AsyncHTMLSession, HTMLResponse
# from requests_html import HTMLSession
from utils import PASS_DOMAIN, geuss_link_url, rm_slash, has_url_html_been_fetched, url_trans, test_blog, bcolors
from itertools import chain
from schema import SiteInfoItem
from site_feature import SiteFeatureTransformer

from is_site_a_zh_i9t_blog import test


asession = AsyncHTMLSession()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
asession.mount('http://', adapter)
asession.mount('https://', adapter)


def save_html(domain, html):
    path = os.path.join('html', f'{domain}.html')
    with open(path, 'w') as f:
        f.write(html)


def get_data(urls):
    res = get_frineds_and_res(urls)
    data = []
    for k, value in res.items():
        url = value['url']
        friends = value.get('friends', [])
        r = value['r']
        site_feature = SiteFeatureTransformer(r=r, url=url, friends=friends)
        if site_feature.feature['has_zh_text'] and test_blog(site_feature.feature):
            site = SiteInfoItem(**site_feature.to_data())
            site_path = f'data/{site.domain}.json'
            with open(site_path, 'w') as f:
                site.save_to_file(f)
            save_html(site.domain, str(r.html.html))
            data.append(site)
        else:
            print(f'{bcolors.WARNING}{url} maybe not personal zh blog{bcolors.ENDC}')
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


def get_frineds_page_link(r: HTMLResponse):
    """
    在首页的 html 中，查询最有可能是友链的页面链接。如果友链内容嵌入在首页中则无法获取。
    """
    friend_page_link = r.html.find("a[href*='friend']")
    friend_page_link.extend(r.html.find("a[title*='友']"))
    if friend_page_link:
        for link in friend_page_link:
            href = link.attrs.get('href')
            if href:
                return url_trans(r.url, href)
        return None
    else:
        return None


def get_frineds_and_res(urls):
    """
    找到给定 url 的友情链接列表,返回 {r,url,friends}
    """
    urls = [url for url in urls if not has_url_html_been_fetched(url)]
    # all_urls = list(chain(*[geuss_link_url(url) for url in urls]))
    all_urls = urls
    res_dict = {}
    try:
        results = asession.run(*[get_url_html(url)
                                 for url in all_urls])

        friend_links = []
        for r in results:
            if r and r.status_code == 200:
                res_dict[urlparse(r.url).netloc] = {
                    'r': r,
                    'url': rm_slash(r.url)
                }
                friend_link = get_frineds_page_link(r)
                if friend_link:
                    friend_links.append(friend_link)
            else:
                pass

        friends_res = asession.run(*[get_url_html(url)
                                     for url in friend_links])

        for r in friends_res:
            if r and r.status_code == 200:
                pass_domain = PASS_DOMAIN + \
                    [urlparse(r.url).netloc]
                friends = list(
                    map(lambda url: rm_slash(url), r.html.absolute_links))

                friends = list(filter(lambda url: all([url.find(
                    pdomain) == -1 for pdomain in pass_domain]) & (urlparse(url).path == ""), set(friends)))

                if res_dict[urlparse(r.url).netloc]:
                    res_dict[urlparse(r.url).netloc]['friends'] = friends

    except Exception as e:
        print(e)
    finally:
        return res_dict


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
