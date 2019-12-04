import os
import json
import re
from urllib.parse import urlparse, urljoin
from utils import rm_slash


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


class SiteFeatureTransformer:
    def __init__(self, url, r, friends, is_zh_i9t_blog=True):
        self.text = r.html.text
        self.r = r
        self.url = rm_slash(url)
        self.friends = friends
        self.is_zh_i9t_blog = is_zh_i9t_blog

    def url_trans(self, url):
        return urljoin(self.url, url) if url.startswith('/') else url

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
    def description(self):
        find_in_meta = self.r.html.find("meta[name='description']", first=True)
        if find_in_meta:
            return find_in_meta.attrs.get('content', '')
        return ''

    @property
    def rss(self):
        # SEE https://github.com/DIYgod/RSSHub-Radar/blob/78ec729b98b2334bebdb75efc53370a9a908af91/src/js/content/utils.js#L39
        RSS_TYPES = [
            'application/rss+xml',
            'application/atom+xml',
            'application/rdf+xml',
            'application/rss',
            'application/atom',
            'application/rdf',
            'text/rss+xml',
            'text/atom+xml',
            'text/rdf+xml',
            'text/rss',
            'text/atom',
            'text/rdf',
        ]
        type_links = self.r.html.find('link[type]')
        if type_links:
            for link in type_links:
                link_type = link.attrs.get("type", None)
                if link_type and link_type in set(RSS_TYPES):
                    return self.url_trans(link.attrs.get("href"))

        a_links = self.r.html.find('a')
        re_check = '([^a-zA-Z]|^)rss([^a-zA-Z]|$)'
        re_rss = r'\/(feed|rss|atom)(\.(xml|rss|atom))?$'
        for a in a_links:
            href = a.attrs.get('href', '')
            title = a.attrs.get('title', '')
            _class = a.attrs.get('class', '')
            if href:
                if any([
                    re.match(re_rss, str(href), re.IGNORECASE),
                    re.match(re_check, str(title), re.IGNORECASE),
                    re.match(re_check, str(_class), re.IGNORECASE)
                ]):
                    return self.url_trans(href)
        return ""

    @property
    def icon(self):
        _default = urljoin(self.url, 'favicon.ico')
        icon = self.r.html.find("link[rel='icon']", first=True)
        shortcut_icon = self.r.html.find(
            "link[rel='shortcut icon']", first=True)

        if icon:
            icon = icon.attrs.get('href', _default)
            # 相对路径时，替换成绝对路径
            icon = self.url_trans(icon)
        if shortcut_icon:
            shortcut_icon = shortcut_icon.attrs.get('href', _default)
            shortcut_icon = self.url_trans(shortcut_icon)
        return icon or shortcut_icon or _default

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
        feature_has = {k: any([re_item.search(self.text, re.IGNORECASE)
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
            "description": self.description,
            "icon": self.icon,
            "friends": self.friends,
            "url": self.url,
            "tld": self.tld,
            "sld": self.sld,
            "is_zh_i9t_blog": self.is_zh_i9t_blog
        }
        return {**feature, **data}

    def save_data_to_file(self):
        p = os.path.join('is_site_a_zh_i9t_blog',
                         'data', f'{self.domain}.json')
        if not os.path.exists(p):
            with open(p, 'w') as f:
                json.dump(self.to_data(), f)
