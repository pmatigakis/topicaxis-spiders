from csv import DictReader
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader

from ..items import GithubProjectWebPageItem, GithubProjectItem


class GithubSpider(scrapy.Spider):
    name = 'github'

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        "DOWNLOAD_DELAY": 0.3,
        "FEED_URI_PARAMS": "topicaxis.utils.github_uri_params",
        "FEED_EXPORT_ENCODING": 'utf-8',
        "FEEDS": {
            '%(github_projects_data)s': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'item_classes': ['topicaxis.items.GithubProjectItem'],
                'postprocessing': [
                    'scrapy.extensions.postprocessing.GzipPlugin'
                ],
            },
            '%(github_project_pages)s': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'item_classes': ['topicaxis.items.GithubProjectWebPageItem'],
                'postprocessing': [
                    'scrapy.extensions.postprocessing.GzipPlugin'
                ],
            }
        }
    }

    def __init__(
        self,
        github_project_urls_file,
        github_projects_data,
        github_project_pages,
        **kwargs
    ):
        super(GithubSpider, self).__init__(**kwargs)
        self.github_project_urls_file = github_project_urls_file
        self.github_projects_data = github_projects_data
        self.github_project_pages = github_project_pages

    def start_requests(self):
        with open(self.github_project_urls_file) as f:
            reader = DictReader(f)
            urls = [row["url"] for row in reader]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        web_page_item_loader = ItemLoader(item=GithubProjectWebPageItem())
        web_page_item_loader.add_value("url", response.request.url)
        web_page_item_loader.add_value(
            "headers", response.headers.to_unicode_dict()
        )
        web_page_item_loader.add_value("content", response.text)
        web_page_item_loader.add_value("status", response.status)
        web_page_item_loader.add_value(
            "downloaded_at", int(datetime.utcnow().timestamp())
        )
        yield web_page_item_loader.load_item()

        github_project_item_loader = ItemLoader(item=GithubProjectItem())
        organization = response.xpath(
            '//*[@id="repository-container-header"]/div[1]/'
            'div[1]/div/span[1]/a/text()'
        ).get()
        if organization:
            organization = organization.strip()
        github_project_item_loader.add_value("organization", organization)

        name = response.xpath(
            '//*[@id="repository-container-header"]/div[1]/div[1]/'
            'div/strong/a/text()'
        ).get()
        if name:
            name = name.strip()
        github_project_item_loader.add_value("name", name)

        description = response.xpath(
            '//*[@id="repo-content-pjax-container"]/div/div/'
            'div[2]/div[2]/div/div[1]/div/p/text()'
        ).get()
        if description:
            description = description.strip()
        github_project_item_loader.add_value("description", description)

        front_page = response.xpath('//*[@id="readme"]/div[2]/article').get()
        if front_page:
            front_page = front_page.strip()
        github_project_item_loader.add_value("frontpage", front_page)

        project_homepage_url = None
        project_homepage_name = response.xpath(
            '//*[@id="repo-content-pjax-container"]/div/div/div[2]/'
            'div[2]/div/div[1]/div/div[1]/span/a'
        ).xpath("text()").get()
        if project_homepage_name:
            project_homepage_name = project_homepage_name.strip()

            project_homepage_url = response.xpath(
                '//*[@id="repo-content-pjax-container"]/div/div/'
                'div[2]/div[2]/div/div[1]/div/div[1]/span/a'
            ).attrib.get("href")

        github_project_item_loader.add_value(
            "homepage",
            {
                "title": project_homepage_name,
                "url": project_homepage_url
            }
        )

        tags = []
        for selector in response.xpath(
                '//a[contains(@class, "topic-tag") and '
                'string-length(text()) > 0 and string-length(@href) > 0]'
        ):
            tags.append({
                "name": selector.xpath("text()").get().strip(),
                "topic_path": selector.attrib["href"]
            })

        github_project_item_loader.add_value(
            "tags",
            tags
        )

        yield github_project_item_loader.load_item()
