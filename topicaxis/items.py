import scrapy


class UrlItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    source_url = scrapy.Field()
    seen_at = scrapy.Field()


class WebPageItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
    headers = scrapy.Field()
    status = scrapy.Field()
    ip_address = scrapy.Field()
    protocol = scrapy.Field()
    downloaded_at = scrapy.Field()


class HackernewsItem(scrapy.Item):
    item_url = scrapy.Field()
    data = scrapy.Field()
    downloaded_at = scrapy.Field()


class RedditItem(scrapy.Item):
    subreddit = scrapy.Field()
    data = scrapy.Field()
    kind = scrapy.Field()
    downloaded_at = scrapy.Field()


class GithubProjectWebPageItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
    headers = scrapy.Field()
    status = scrapy.Field()
    downloaded_at = scrapy.Field()


class GithubProjectItem(scrapy.Item):
    organization = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    frontpage = scrapy.Field()
    homepage = scrapy.Field()
    tags = scrapy.Field()
