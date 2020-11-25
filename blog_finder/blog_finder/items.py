# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import json
from urllib.parse import urlparse
from dataclasses import dataclass, field, asdict
from typing import List, Optional

# from datafiles import datafile


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

    has_archive: bool = False
    has_tag: bool = False
    has_category: bool = False
    has_about: bool = False
    has_theme: bool = False
    has_zh_text: bool = False
    has_blog_text: bool = False

    is_zh_i9t_blog: bool = True

    def __post_init__(self):
        if not self.domain:
            self.domain = urlparse(self.url).netloc
