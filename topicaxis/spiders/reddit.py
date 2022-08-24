from datetime import datetime

import scrapy
from scrapy.http import JsonRequest
from scrapy.loader import ItemLoader

from ..items import RedditItem


class ReddirSpider(scrapy.Spider):
    name = "reddit"

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_URI_PARAMS": "topicaxis.utils.reddit_uri_params",
        "FEED_EXPORT_ENCODING": 'utf-8',
        "FEEDS": {
            '%(output)s': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'item_classes': ['topicaxis.items.RedditItem'],
                'postprocessing': [
                    'scrapy.extensions.postprocessing.GzipPlugin'
                ],
            }
        }
    }

    def __init__(self, subreddit, output, max_depth: int = 10, **kwargs):
        super(ReddirSpider, self).__init__(**kwargs)

        self.subreddit = subreddit
        self.output = output
        self.max_depth = int(max_depth)

    def start_requests(self):
        yield JsonRequest(
            f"https://www.reddit.com/r/{self.subreddit}.json?limit=100",
            method="GET",
            callback=self.process_page,
            cb_kwargs={
                "depth": 1
            }
        )

    def process_page(self, response, depth):
        page = response.json()
        for item in page["data"]["children"]:
            reddit_item_loader = ItemLoader(item=RedditItem())
            reddit_item_loader.add_value("subreddit", self.subreddit)
            reddit_item_loader.add_value("kind", item["kind"])
            reddit_item_loader.add_value("data", item["data"])
            reddit_item_loader.add_value(
                "downloaded_at", int(datetime.utcnow().timestamp())
            )

            yield reddit_item_loader.load_item()

        after = page["data"]["after"]
        if depth < self.max_depth and after:
            yield JsonRequest(
                f"https://www.reddit.com/r/{self.subreddit}.json?"
                f"limit=100&after={after}",
                method="GET",
                callback=self.process_page,
                cb_kwargs={
                    "depth": depth+1
                }
            )
