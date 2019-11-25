from urllib.parse import urljoin

PASS_URL = ["youtube.com", "wikipedia.org", "facebook.com", "twitter.com", "zhihu.com",
            "weibo.com", "github.com", "reactjs.org", "material-ui.com", "gatsbyjs.org",
            "steamcommunity.com", "segmentfault.com", "netlify.com", "wordpress.com", "taobao.com",
            "gohugo.io", "hexo.io", "gov.cn", "cloudflare.com", "ubuntu.com",
            "docker.com", "jekyll.com", "localhost"
            ]


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
