# Topicaxis spiders

This repository contains the web crawlers used by Topicaxis.

## Configuration

Open `topicaxis/settings.py` and set the required configuration variables.

| Name       | Description                      |
|------------|----------------------------------|
| BOT_NAME   | The name of the crawler          |
| USER_AGENT | The web crawler user agent value |

## Build the docker image

```bash
docker build -t topicaxis/spiders .
```

## Run a spider using docker

```bash
docker container run -d \
--mount type=bind,source=/home/topicaxis/topicaxis-spiders/volumes/dumps,target=/crawlers/dumps \
--mount type=bind,source=/home/topicaxis/topicaxis-spiders/volumes/input,target=/crawlers/input \
--rm -it topicaxis/spiders \
scrapy crawl webpages -a sources_file=/crawlers/input/sources.csv -a urls_output=/crawlers/dumps/urls.jl.gz -a web_pages_output=/crawlers/dumps/web_pages.jl.gz
```

```bash
docker container run -d \
--mount type=bind,source=/home/topicaxis/topicaxis-spiders/volumes/dumps,target=/crawlers/dumps \
--rm -it topicaxis/spiders \
scrapy crawl hackernews -a output=/crawlers/dumps/hackernews.jl.gz
```

```bash
docker container run -d \
--mount type=bind,source=/home/topicaxis/topicaxis-spiders/volumes/dumps,target=/crawlers/dumps \
--rm -it topicaxis/spiders \
scrapy crawl github -a github_project_urls_file=/crawlers/dumps/github_project_urls.csv -a github_projects_data=/crawlers/dumps/github_projects_data.jl.gz -a github_project_pages=/crawlers/dumps/github_project_pages.jl.gz
```
