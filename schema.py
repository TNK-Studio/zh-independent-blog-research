import json

from typing import List, Optional
from dataclasses import dataclass, field, asdict
# from datafiles import datafile
from urllib.parse import urlparse


# @datafile("data/{self.domain}.json")
@dataclass(init=True)
class SiteInfoItem:
    url: str = ''
    name: Optional[str] = ''
    domain: Optional[str] = ''
    icon: Optional[str] = ''
    rss: Optional[str] = ''
    generator: Optional[str] = ''
    description: Optional[str] = ''
    friends: Optional[List[str]] = field(default_factory=list)
    # not use
    host_server: Optional[str] = ''
    comment_server: Optional[str] = ''

    # features
    tld: Optional[str] = ''
    sld: Optional[str] = ''
    len_friends: int = 0
    has_rss: bool = False
    has_generator: bool = False
    has_archive: bool = False
    has_tag: bool = False
    has_category: bool = False
    has_about: bool = False
    has_theme: bool = False
    has_zh_text: bool = False
    has_blog_text: bool = False

    # y
    is_zh_i9t_blog: bool = True

    def __post_init__(self):
        if not self.domain:
            self.domain = urlparse(self.url).netloc

    def save_to_file(self, f):
        r = asdict(self)
        # print(r)
        json.dump(r, f)
        print(f"update:{self.domain}")


if __name__ == "__main__":
    site = SiteInfoItem(url="https://gine.me")
    site.name = "Mayne's Blog"
    site.domain = 'gine.me'
    site.rss = "/feed"
    site.host_server = 'netlify'
    site.comment_server = 'diqus'
    site.friends = [
        'https://ruterly.com'
    ]
    # site.save_to_file()
