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

from is_site_a_zh_i9t_blog import test


asession = AsyncHTMLSession()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
asession.mount('http://', adapter)
asession.mount('https://', adapter)


re_zh_text = zh_re = re.compile('[\u4e00-\u9fa5]')
re_archive_zh = re.compile('归档')
re_archive_en = re.compile('archive')
re_tag_zh = re.compile('标签')
re_tag_en = re.compile('tag')
re_cate_zh = re.compile('分类')
re_cate_en = re.compile('categor')
re_about_zh = re.compile('关于')
re_about_en = re.compile('about')
re_theme_en = re.compile('theme')
re_blog_text_zh = re.compile('博客')
re_blog_text_en = re.compile('blog')

re_map = {
    "has_archive": [re_archive_en, re_about_zh],
    "has_tag": [re_tag_en, re_about_zh],
    "has_category": [re_cate_en, re_cate_zh],
    "has_about": [re_about_zh, re_about_en],
    "has_theme": [re_theme_en],
    "has_zh_text": [re_zh_text],
    "has_blog_text": [re_blog_text_en, re_blog_text_zh]
}


# 标题中出现这些关键词时，基本上不会是个人博客
BLACK_WORDS = set({
    "SEO", "官方", "导航", "网址"
})


class SiteFeatureTransformer:
    def __init__(self, url, r, friends):
        self.text = r.html.text
        self.r = r
        self.url = url
        self.friends = friends

    @property
    def domain(self):
        return urlparse(self.url).netloc

    @property
    def tld(self):
        return self.domain.split(".")[-1]

    @property
    def sld(self):
        return self.domain.split(".")[-2]

    @property
    def name(self):
        title = self.r.html.find('title', first=True)
        if title:
            return title.text
        else:
            return 'unknown'

    @property
    def rss(self):
        pass
        return ""

    @property
    def generator(self):
        find_in_meta = self.r.html.find("meta[name='generator']", first=True)
        if find_in_meta:
            return find_in_meta.attrs.get('content', 'unknown')

        find_in_html_text = self.r.html.search("Powered by{}<a{}>{}</a>")
        if find_in_html_text:
            return find_in_html_text[2]
        else:
            return 'unknown'

    @property
    def feature(self):
        feature_has = {k: any([re_item.search(self.text)
                               for re_item in res]) for k, res in re_map.items()}
        feature_has["has_generator"] = bool(self.generator != 'unknown')
        feature_has["has_rss"] = bool(self.rss)

        feature = {
            "len_friends":  len(self.friends),
            # "tld": self.tld,
            # "sld": self.sld,
        }
        return {**feature_has, **feature}

    def to_data(self):
        feature = self.feature
        data = {
            "domain": self.domain,
            "name": self.name,
            "rss": self.rss,
            "generator": self.generator,
            "friends": self.friends,
            "url": self.url,
            "tld": self.tld,
            "sld": self.sld
        }
        return {**feature, **data}


def save_html(domain, html):
    path = os.path.join('html', f'{domain}.html')
    with open(path, 'w') as f:
        f.write(html)


def get_data(urls):
    res = get_frineds_and_res(urls)
    data = []
    for url, friends, r in res:
        site_feature = SiteFeatureTransformer(r=r, url=url, friends=friends)
        if site_feature.feature['has_zh_text'] and test(site_feature.feature) :
            site = SiteInfoItem(**site_feature.to_data())
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
