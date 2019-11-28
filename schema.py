from typing import List, Optional
from dataclasses import dataclass, field
from datafiles import datafile
from urllib.parse import urlparse


@datafile("data/{self.domain}.json")
@dataclass(init=True)
class SiteInfoItem:
    url: str = ''
    name: Optional[str] = ''
    domain: Optional[str] = ''
    rss: Optional[str] = ''
    generator: Optional[str] = ''
    friends: Optional[List[str]] = field(default_factory=list)
    #
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


if __name__ == "__main__":
    site = SiteInfoItem(url="https://gine.me")
    site.name = "Mayne's Blog"
    site.rss = "/feed"
    site.host_server = 'netlify'
    site.comment_server = 'diqus'
    site.friends = [
        'https://ruterly.com'
    ]
