FROM python:3.8.13

WORKDIR /app

ADD topicaxis /app/topicaxis
COPY pyproject.toml /app
COPY poetry.lock /app
COPY scrapy.cfg /app

RUN pip install poetry==1.1.13
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
