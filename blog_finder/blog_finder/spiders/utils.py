import os
import json

from urllib.parse import urljoin, urlparse


# 恶心
BLACK_LIST = [
    "1588.tv"
]

# 整个 alexa top 100 排名？
PASS_DOMAIN = BLACK_LIST + ["youtube.com", "wikipedia.org", "facebook.com", "twitter.com", "zhihu.com",
                            "weibo.com", "github.com", "reactjs.org", "material-ui.com", "gatsbyjs.org",
                            "steamcommunity.com", "segmentfault.com", "netlify.com", "wordpress.com", "taobao.com",
                            "gohugo.io", "hexo.io", "gov.cn", "cloudflare.com", "ubuntu.com",
                            "docker.com", "jekyll.com", "localhost", "blogspot.com", "tmall.com",
                            "wordpress.cn", "wordpress.org", "baidu.com", "blogger.com", "qq.com",
                            "edu.cn", "edu", "gov"
                            ]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def url_trans(base_url, url: str):
    if url.startswith('/'):
        return urljoin(base_url, url)
    else:
        return url


def has_url_html_been_fetched(url):
    path = f"{urlparse(url).netloc}.html"
    return os.path.exists(path)


def geuss_link_url(url):
    """
    猜测给定 url 的友链地址
    """
    # 默认从这些页面找
    geuss_path = ["link", "friend"]
    with_s = map(lambda x: x+'s', geuss_path)
    geuss_path.extend(list(with_s))

    # 其次是关于页面
    geuss_path += ["about"]
    with_html = map(lambda x: x+'.html', geuss_path)
    geuss_path.extend(list(with_html))

    return list(map(lambda path: urljoin(url, path), geuss_path)) + [url]


def rm_slash(url):
    if url.endswith('/'):
        return url[:-1]
    return url
