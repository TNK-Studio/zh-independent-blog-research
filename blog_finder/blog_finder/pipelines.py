# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
from vika import Vika
from .items import SiteInfoItem

token = os.environ['VIKA_API_TOKEN']
dst_id = os.environ['VIKA_BLOG_FINDER_DST_ID']


class BlogFinderPipeline:
    def __init__(self):
        vika = Vika(token)
        self.datasheet = vika.datasheet(dst_id)

    def process_item(self, item, spider):
        _item = ItemAdapter(item)
        try:
            self.datasheet.records.create({
                "domain": _item['domain'],
                "url": _item["url"],
                "name": _item['name'],
                "icon": _item['icon'],
                "rss": _item['rss'] if _item['rss'] else None,
                "generator": _item['generator'],
                "description": _item['description'],
                "friend_links": ",".join(_item['friends']),
                "has_archive": _item["has_archive"],
                "has_tag": _item["has_tag"],
                "has_category": _item["has_category"],
                "has_about": _item["has_about"],
                "has_theme": _item["has_theme"],
                "has_zh_text": _item["has_zh_text"],
                "has_blog_text": _item["has_blog_text"]
            })
        except Exception as e:
            print(e)
        return item
