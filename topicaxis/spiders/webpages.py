from csv import DictReader
from datetime import datetime

import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.loader import ItemLoader

from ..items import UrlItem, WebPageItem


class SourcesSpider(scrapy.Spider):
    name = 'webpages'

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_URI_PARAMS": "topicaxis.utils.webpages_uri_params",
        "FEED_EXPORT_ENCODING": 'utf-8',
        "FEEDS": {
            '%(urls_output)s': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'item_classes': ['topicaxis.items.UrlItem'],
                'postprocessing': [
                    'scrapy.extensions.postprocessing.GzipPlugin'
                ],
            },
            '%(web_pages_output)s': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'item_classes': ['topicaxis.items.WebPageItem'],
                'postprocessing': [
                    'scrapy.extensions.postprocessing.GzipPlugin'
                ],
            }
        }
    }

    def __init__(self, sources_file, urls_output, web_pages_output, **kwargs):
        super(SourcesSpider, self).__init__(**kwargs)
        self.sources_file = sources_file
        self.urls_output = urls_output
        self.web_pages_output = web_pages_output

    def start_requests(self):
        with open(self.sources_file) as f:
            reader = DictReader(f)
            urls = [row["url"] for row in reader]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        web_page_item_loader = ItemLoader(item=WebPageItem())
        web_page_item_loader.add_value("url", response.request.url)
        web_page_item_loader.add_value(
            "headers", response.headers.to_unicode_dict()
        )
        web_page_item_loader.add_value("content", response.text)
        web_page_item_loader.add_value("status", response.status)
        web_page_item_loader.add_value("protocol", response.protocol)
        web_page_item_loader.add_value("ip_address", str(response.ip_address))
        web_page_item_loader.add_value(
            "downloaded_at", int(datetime.utcnow().timestamp())
        )
        yield web_page_item_loader.load_item()

        link_extractor = LxmlLinkExtractor()
        for link in link_extractor.extract_links(response):
            url_item_loader = ItemLoader(item=UrlItem())
            url_item_loader.add_value("url", link.url)
            url_item_loader.add_value("title", link.text.strip())
            url_item_loader.add_value("source_url", response.request.url)
            url_item_loader.add_value(
                "seen_at", int(datetime.utcnow().timestamp())
            )
            yield url_item_loader.load_item()
