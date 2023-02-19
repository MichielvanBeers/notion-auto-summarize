# Notion automated summarization

## Introduction
This is a simple docker container that will automatically summarize any content on a page in Notion. It works by retrieving all the pages in a database have not been added for X days and don't have any content in the Summary field. It then sends the content of the page to the [OpenAI API](https://beta.openai.com/overview). This will use machine learning to automatically summarize the content. The content will the be entered in the Summary field.

## Prerequisites
1. An account at [OpenAI](https://beta.openai.com/).
2. An API key for OpenAI that can be retrieved [here](https://beta.openai.com/account/api-keys).
3. An account at [Notion](https://www.notion.so/).
4. An integration and API key for Notion. Instructions can be found [here](https://developers.notion.com/docs/getting-started).
5. An environment with [docker](https://docs.docker.com/get-docker/) installed.

## Installation
Installation and running this scripts can be done through either Docker or Docker Compose.

### Docker example
```
docker run --name some-name-for-your-container -e NOTION_TOKEN=secret_12345678 -e DATABASE_ID=d82973h2kwldj20239e1 -e OPEN_AI_TOKEN=sk-nd92e2109js09219udj9101oj1290 SUMMARIZATION_FIELD=Summary DAYS_BEFORE_SUMMARY=7 RUN_FREQUENCY=15 michielvanbeers/notion-auto-summarize
```

### Docker compose example
```
version: '3'

services:
  notion-auto-summarize:
    image: michielvanbeers/notion-auto-summarize
    restart: unless-stopped
    environment:
      - NOTION_TOKEN=secret_12345678
      - DATABASE_ID=d82973h2kwldj20239e1
      - OPEN_AI_TOKEN=sk-nd92e2109js09219udj9101oj1290
      - SUMMARIZATION_FIELD=Summary
      - DAYS_BEFORE_SUMMARY=7
      - RUN_FREQUENCY=15 # Optional
```

### Environment variables
* **NOTION_TOKEN**: API token to integrate with Notion. Don't forget to allow your intergration access to your database
* **DATABASE_ID**: ID of the database that you want to scan
* **OPEN_AI_TOKEN**: API token to allow communication with OpenAI
* **SUMMARIZATION_FIELD**: Field where the summary of the page will be written to
* **DAYS_BEFORE_SUMMARY**: The amount of days that need to have passed before the summary of the article is created
* **RUN_FREQUENCY**: Determines after how many minutes a new scan is done (in minutes)
