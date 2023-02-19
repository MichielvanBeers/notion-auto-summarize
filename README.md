# Notion automated summarization

## Introduction
This is a simple python script that will automatically summarize any content on a page in Notion. It works by retrieving all the pages in a database that are more than X days old and don't have any content in the Summary field. It then sends the content of the page to the [OpenAI API](https://beta.openai.com/overview). This will use machine learning to automatically summarize the content. The content will the be entered in the Summary field.

## Prerequisites
1. An account at [OpenAI](https://beta.openai.com/)
2. An API key for OpenAI that can be retrieved [here](https://beta.openai.com/account/api-keys)
3. An account at [Notion](https://www.notion.so/)
4. An intergration and API key for Notion. Instructions can be found [here](https://developers.notion.com/docs/getting-started)
5. An environment with python 3 and [the openai pip package](https://pypi.org/project/openai/) installed

## Running the script
The scripts expects three parameters, in fixed order:
1. Notion API token
2. Database ID of the Notion database that you want to summarize:
```
https://www.notion.so/myworkspace/a8aec43384f447ed84390e8e42c2e089?v=...
                                  |--------- Database ID --------|
```

3. OpenAI API token

Then run the script by entering in your terminal `python3 Summarize.py 'NOTION_TOKEN' 'DATABASE_ID' 'OPEN_AI_TOKEN'`
  
## Automatization
You can let the script run automatically every 15 minutes be adding it to your crontab (in Linux)
```
*/15 * * * * cd /[LOCATION OF THE SCRIPT]; /usr/bin/python3 ./Summarize.py 'NOTION_TOKEN' 'DATABASE_ID' 'OPEN_AI_TOKEN'
```
