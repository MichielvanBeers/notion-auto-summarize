import requests
import os
from src.notion import Notion
from src.openai_request import OpenAIRequest

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]
OPEN_AI_TOKEN = os.environ["OPEN_AI_TOKEN"]
SCAN_FREQUENCY = (
    os.environ["SCAN_FREQUENCY"] if "SCAN_FREQUENCY" in os.environ else None
)
SUMMARIZATION_FIELD = os.environ["SUMMARIZATION_FIELD"]
DAYS_BEFORE_SUMMARY = os.environ["DAYS_BEFORE_SUMMARY"]
HEADERS = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


openai_request = OpenAIRequest(OPEN_AI_TOKEN)
notion = Notion(HEADERS, 7)

notion_content = notion.read_database(DATABASE_ID)

for page in notion_content:
    try:
        page_text = notion.read_page_content(page["id"])
        summary = openai_request.get_summary(page_text)
        notion.add_summary_to_page(page["id"], summary)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise SystemExit(e)
