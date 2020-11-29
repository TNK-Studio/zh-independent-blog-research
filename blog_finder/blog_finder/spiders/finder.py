import scrapy
from requests_html import HTML, HTMLSession
from .utils import PASS_DOMAIN, geuss_link_url, rm_slash, has_url_html_been_fetched, url_trans, bcolors
from .site_feature import SiteFeatureTransformer
from urllib.parse import urlparse
from .seed import seed
from .is_zh_i9t_blog import is_zh_i9t_blog

session = HTMLSession()

seed_set = set([urlparse(url).netloc for url in seed])


class BlogSpider(scrapy.Spider):
    name = "blogs"
    start_urls = seed

    def filter(self, site):
        # white list
        if site.domain in seed_set:
            return True
        if len(site.friends) > 75:
            return False
        if is_zh_i9t_blog(site.feature):
            return True
        return False

    def parse(self, response):
        html = HTML(url=response.url, html=response.text)
        friends = self.get_friends(html)
        site_feature = SiteFeatureTransformer(
            url=html.url, html_text=response.text, friends=friends)

        if self.filter(site_feature):
            yield site_feature.to_data()
            yield from response.follow_all(friends, callback=self.parse)

    def get_friends(self, html):
        friends_link = self.get_friends_page_link(html)
        friends = []
        if friends_link:
            r = session.get(friends_link)
            pass_domain = PASS_DOMAIN + \
                [urlparse(r.url).netloc]
            friends = list(
                map(lambda url: rm_slash(url), r.html.absolute_links))

            friends = list(filter(lambda url: all([url.find(
                pdomain) == -1 for pdomain in pass_domain]) & (urlparse(url).path == ""), set(friends)))

        return friends

    def get_friends_page_link(self, html):
        """
        在首页的 html 中，查询最有可能是友链的页面链接。如果友链内容嵌入在首页中则无法获取。
        """
        friend_page_link = html.find("a[href*='friend']")
        friend_page_link.extend(html.find("a[href*='link']"))
        friend_page_link.extend(html.find("a[title*='友']"))
        if friend_page_link:
            for link in friend_page_link:
                href = link.attrs.get('href')
                if href:
                    return url_trans(html.url, href)
            return None
        else:
            return None
