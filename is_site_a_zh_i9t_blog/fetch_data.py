import os
import requests
import re
import json

from dataclasses import dataclass
from urllib.parse import urljoin
from urllib.parse import urlparse
from requests_html import AsyncHTMLSession, HTML
from utils import PASS_DOMAIN, geuss_link_url, rm_slash, has_url_html_been_fetched
from itertools import chain
from multiprocessing import cpu_count, Pool, Manager, Queue, TimeoutError
from site_feature import SiteFeatureTransformer

asession = AsyncHTMLSession()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
asession.mount('http://', adapter)
asession.mount('https://', adapter)



def save_html(domain, html):
    path = os.path.join('html', f'{domain}.html')
    with open(path, 'w') as f:
        f.write(html)


def get_data(urls, is_zh_i9t_blog=False):
    res = get_frineds_and_res(urls, is_zh_i9t_blog)
    data = []
    for url, friends, r in res:
        site_feature = SiteFeatureTransformer(
            r=r, url=url, friends=friends, is_zh_i9t_blog=is_zh_i9t_blog)
        site = site_feature.to_data()
        site_feature.save_data_to_file()
        save_html(site['domain'], str(r.html.html))
        data.append(site)
    return data


def get_url_html(url):
    async def f():
        # print("get:{}".format(url))
        try:
            # print(url)
            r = await asession.get(url, timeout=10)
            return r
        except requests.exceptions.ConnectTimeout:
            # print("{} 链接超时，不可访问".format(url))
            pass
        except:
            pass
            # print("{} 链接错误，不可访问".format(url))
    return f


def get_frineds_and_res(urls, is_zh_i9t_blog=False):
    """
    找到给定 url 的友情链接列表,返回友链 & 友链页面 html
    """
    all_urls = []
    # urls = [url for url in urls if not has_url_html_been_fetched(url)]
    if is_zh_i9t_blog:
        all_urls = list(chain(*[geuss_link_url(url) for url in urls]))
    else:
        all_urls = urls
    res = []
    try:
        results = asession.run(*[get_url_html(url)
                                 for url in all_urls])

        for url in urls:
            friends = []
            index_rhtml = None
            for r in results:
                if r:
                    # print(r.status_code)
                    if friends and index_rhtml:
                        break
                    elif r.status_code == 200 and urlparse(r.url).netloc == urlparse(url).netloc:
                        if not friends:
                            # + PASS_DOMAIN
                            pass_domain = [
                                urlparse(r.url).netloc] + PASS_DOMAIN
                            out_links = [link for link in r.html.absolute_links if urlparse(
                                link).netloc != urlparse(url).netloc]
                            friends = list(
                                map(lambda url: rm_slash(url), out_links))
                            friends = list(filter(lambda url: all([url.find(
                                pdomain) == -1 for pdomain in pass_domain]) & (urlparse(url).path == ""), set(friends)))

                            print(friends)
                        if not index_rhtml and rm_slash(r.url) == rm_slash(url):
                            index_rhtml = r
                else:
                    pass
            # print(url, friends, index_rhtml)
            if is_zh_i9t_blog:
                if friends and index_rhtml:
                    res.append((url, friends, index_rhtml))
            elif index_rhtml:
                res.append((url, friends, index_rhtml))

    except Exception as e:
        print(e)
    finally:
        # print(res)
        return res


def main():
    p0 = os.path.join(os.path.dirname(__file__), 'top500site.json')
    with open(p0, 'r') as f:
        urls = json.load(f)
        args = [(urls[i:i + 8], 0) for i in range(0, len(urls), 8)]
        for links, flag in args:
            get_data(links, flag)

    p1 = os.path.join(os.path.dirname(__file__), 'top100zh_site.json')
    with open(p1, 'r') as f:
        urls = json.load(f)
        args = [(urls[i:i + 8], 0) for i in range(0, len(urls), 8)]
        for links, flag in args:
            get_data(links, flag)

    p2 = os.path.join(os.path.dirname(__file__), 'zh_i9t_blog_list.json')
    with open(p2, 'r') as f:
        urls = json.load(f)
        args = [(urls[i:i + 8], 1) for i in range(0, len(urls), 8)]
        for links, flag in args:
            get_data(links, flag)

    data_path = os.path.join(os.path.dirname(__file__), 'data')

    data_set_file_path = os.path.join(
        os.path.dirname(__file__), 'dataset.json')
    r = []
    for ddir in iter(os.listdir(data_path)):
        with open(os.path.join(data_path, ddir)) as f:
            d = json.load(f)
            r.append(d)
    with open(data_set_file_path, 'w') as f:
        json.dump(r, f)
