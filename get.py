from urllib.parse import urljoin
from urllib.parse import urlparse
from requests_html import AsyncHTMLSession
# from requests_html import HTMLSession
from utils import PASS_DOMAIN, geuss_link_url, rm_slash
from itertools import chain
from schema import SiteInfoItem
import requests
import re

asession = AsyncHTMLSession()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
asession.mount('http://', adapter)
asession.mount('https://', adapter)


zh_re = re.compile('[\u4e00-\u9fa5]')


# 标题中出现这些关键词时，基本上不会是个人博客
BLACK_WORDS = set({
    "SEO", "官方", "导航", "网址"
})


def is_zh_blog(friends, generator, has_zh_text, name):
    if not has_zh_text:
        return False
    if any([name.find(word) > -1 for word in BLACK_WORDS]):
        return False
    if generator == 'unknown' and len(friends) > 30:
        # fixme 需要更多的特征判断一个站点是不是个人博客
        return False
    return True


def has_zh_text(r):
    if zh_re.search(r.html.text):
        return True
    else:
        return False


def get_data(urls):
    res = get_frineds_and_res(urls)
    data = []
    for url, friends, r in res:
        generator = get_generator(r)
        name = get_name(r)
        _has_zh_text = has_zh_text(r)
        if is_zh_blog(friends, generator, _has_zh_text, name):
            data.append(SiteInfoItem(url=url, friends=friends,
                                     name=name, generator=generator))
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


def get_name(r):
    title = r.html.find('title', first=True)
    if title:
        return title.text
    else:
        return 'unknown'


def get_generator(r):
    find_in_meta = r.html.find("meta[name='generator']", first=True)
    if find_in_meta:
        return find_in_meta.attrs['content']

    find_in_html_text = r.html.search("Powered by{}<a{}>{}</a>")
    if find_in_html_text:
        return find_in_html_text[2]
    else:
        return 'unknown'


def get_frineds_and_res(urls):
    """
    找到给定 url 的友情链接列表,返回友链 & 友链页面 html
    """
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

    get_data(urls)
