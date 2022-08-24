from datetime import datetime

import scrapy
from scrapy.http import JsonRequest
from scrapy.loader import ItemLoader

from ..items import HackernewsItem


class HackernewsSpider(scrapy.Spider):
    name = "hackernews"

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_URI_PARAMS": "topicaxis.utils.hackernews_uri_params",
        "FEED_EXPORT_ENCODING": 'utf-8',
        "FEEDS": {
            '%(output)s': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'item_classes': ['topicaxis.items.HackernewsItem'],
                'postprocessing': [
                    'scrapy.extensions.postprocessing.GzipPlugin'
                ],
            }
        }
    }

    def __init__(self, output, **kwargs):
        super(HackernewsSpider, self).__init__(**kwargs)
        self.output = output

    def start_requests(self):
        yield JsonRequest(
            "https://hacker-news.firebaseio.com/v0/newstories.json",
            method="GET",
            callback=self.process_new_story_ids
        )

    def process_new_story_ids(self, response):
        for item_id in response.json():
            yield JsonRequest(
                f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json",
                method="GET",
                callback=self.process_item_id
            )

    def process_item_id(self, response):
        hackernews_item_loader = ItemLoader(item=HackernewsItem())
        hackernews_item_loader.add_value("item_url", response.request.url)
        hackernews_item_loader.add_value("data", response.json())
        hackernews_item_loader.add_value(
            "downloaded_at", int(datetime.utcnow().timestamp())
        )

        yield hackernews_item_loader.load_item()
