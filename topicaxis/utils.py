def webpages_uri_params(params, spider):
    return {
        **params,
        "sources_file": spider.sources_file,
        "urls_output": spider.urls_output,
        "web_pages_output": spider.web_pages_output,
    }


def hackernews_uri_params(params, spider):
    return {
        **params,
        "output": spider.output,
    }


def reddit_uri_params(params, spider):
    return {
        **params,
        "subreddit": spider.subreddit,
        "output": spider.output,
        "max_depth": spider.max_depth,
    }


def github_uri_params(params, spider):
    return {
        **params,
        "github_project_urls_file": spider.github_project_urls_file,
        "github_projects_data": spider.github_projects_data,
        "github_project_pages": spider.github_project_pages,
    }
