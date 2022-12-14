import requests
import json
import openai
import logging
import os
import datetime
import sys
import re

# Setup logging
log_file = os.getcwd() + '/output.log'
logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Arguments [Notion Token] [Database ID] [OpenAI Token]
NOTION_TOKEN = sys.argv[1]
DATABASE_ID = sys.argv[2]
OPEN_AI_TOKEN = sys.argv[3]
HEADERS = {
    "Authorization": "Bearer " + str(NOTION_TOKEN),
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
PAGE_SIZE =  10
LAST_UPDATE_DAYS_AGO = 7

def read_database(database_id, headers):
    read_url = f"https://api.notion.com/v1/databases/{database_id}/query"

    current_date_time = datetime.datetime.now()
    date_time_one_week_ago = current_date_time - datetime.timedelta(days=LAST_UPDATE_DAYS_AGO)
    date_time_one_week_ago_iso = date_time_one_week_ago.isoformat()

    logging.info(f"Sending request for {PAGE_SIZE} pages that are updated {LAST_UPDATE_DAYS_AGO} days ago")

    request_body = {
        "page_size": PAGE_SIZE,
        "filter": {
            "and": [
                {
                    "property": "Summary",
                    "rich_text": {
                        "is_empty": True
                    }
                },
                {
                    "timestamp": "last_edited_time",
                    "last_edited_time": {
                        "before": date_time_one_week_ago_iso
                    }
                },
            ]
        }
    }

    data = json.dumps(request_body)

    res = requests.request("POST", read_url, headers=headers, data=data)

    if not res.ok:
        logging.error(f"An error occurred. Response code: {res.status_code}. Response body: {res.text}")
        sys.exit()

    response_json = res.json()

    pages = response_json['results']

    if pages == []:
        logging.info("The query didn't match any results")

    logging.info(f"Pages results: {pages}")

    return pages

def read_page_content(page_id, headers):
    read_url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    res = requests.request("GET", read_url, headers=headers)
    data = res.json()
    results = data['results']

    page_content = ''

    for block in results:
        if block['type'] == 'paragraph':
            for text in block['paragraph']['rich_text']:
                page_content += text['plain_text'] + "\n"

    return page_content


def get_summary(text):

    openai.api_key = str(OPEN_AI_TOKEN)

    body = text + "\n\n Tl;dr"

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=body,
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    result = ""

    for content in response['choices']:
        result += content['text']

    clean_result = result.replace('\n', ' ').replace('\r', '').lstrip()

    result_without_colon = re.sub(r"^\W+", "", clean_result)

    logging.info(f"Summary result: {result_without_colon}")

    return(result_without_colon)


def add_summary_to_page(page_id, summary, headers):
    page_url = f"https://api.notion.com/v1/pages/{page_id}"

    update_data = {
        "properties": {
            "Summary": {
                "rich_text": [
                    {
                        "text": {
                            "content": summary
                        }
                    }
                ]
            }
        }
    }

    data = json.dumps(update_data)

    response = requests.request(
        "PATCH", page_url, headers=headers, data=data)

    logging.info(f"Response PATCH request: {response.text}")

notion_content = read_database(DATABASE_ID, HEADERS)

for page in notion_content:
    try:
        page_text = read_page_content(page['id'], HEADERS)
        summary = get_summary(page_text)
        add_summary_to_page(page['id'], summary, HEADERS)
    except:
        logging.critical(f"An error occurred")