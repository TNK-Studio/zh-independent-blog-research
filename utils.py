import os
import json

from urllib.parse import urljoin, urlparse


# 整个 alexa top 100 排名？
PASS_DOMAIN = ["youtube.com", "wikipedia.org", "facebook.com", "twitter.com", "zhihu.com",
               "weibo.com", "github.com", "reactjs.org", "material-ui.com", "gatsbyjs.org",
               "steamcommunity.com", "segmentfault.com", "netlify.com", "wordpress.com", "taobao.com",
               "gohugo.io", "hexo.io", "gov.cn", "cloudflare.com", "ubuntu.com",
               "docker.com", "jekyll.com", "localhost", "blogspot.com", "tmall.com",
               "wordpress.cn", "wordpress.org", "baidu.com", "blogger.com"
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


def to_json_data():
    data = []
    for itemdir in iter(os.listdir('data')):
        with open('data/'+itemdir, 'r') as f:
            data.append(json.load(f))

    with open('site/src/data.json', 'w') as f:
        json.dump(data, f)
    # return data


def to_graphql_data():
    data = {'nodes': [], 'edges': []}

    url_set = set()
    url_friends_map = {}
    for itemdir in iter(os.listdir('data')):
        with open('data/'+itemdir, 'r') as f:
            item = json.load(f)
            url_set.add(item['url'])
            data['nodes'].append({
                'id': item['url'],
                'label': item['url'],
                'title': item['name'],
                'group': item['url'].split(".")[-1]
            })
            url_friends_map[item['url']] = item['friends']

    for url, friends in url_friends_map.items():
        for friend in friends:
            if friend in url_set:
                data['edges'].append({
                    'from': url,
                    "to": friend
                })

    with open('site/src/graph.json', 'w') as f:
        json.dump(data, f)
