from typing import List, Optional
from dataclasses import dataclass, field
from datafiles import datafile
from urllib.parse import urlparse


@datafile("data/{self.domain}.json")
# @dataclass
class SiteInfoItem:
    url: str = ''
    name: Optional[str] = None
    domain: str = field(init=False)
    dtl: str = field(init=False)
    rss: Optional[str] = None
    generator: Optional[str] = None
    host_server: Optional[str] = None
    comment_server: Optional[str] = None
    friends: Optional[List[str]] = None

    def __post_init__(self):
        self.domain = urlparse(self.url).netloc
        self.dtl = self.domain.split(".")[-1]


if __name__ == "__main__":
    site = SiteInfoItem(url="https://gine.me")
    site.name = "Mayne's Blog"
    site.rss = "/feed"
    site.host_server = 'netlify'
    site.comment_server = 'diqus'
    site.friends = [
        'https://ruterly.com'
    ]
