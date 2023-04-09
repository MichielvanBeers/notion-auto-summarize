import json
import requests
from datetime import datetime, timedelta
from typing import Dict


class Notion:
    """
    Class to retrieve database content and page content of a Notion Database.
    """

    def __init__(self, headers: Dict[str, str], created_before: str | int) -> None:
        self.created_before = created_before
        self.headers = headers

    def read_database(self, database_id: str) -> list[dict]:
        read_url = f"https://api.notion.com/v1/databases/{database_id}/query"

        current_date_time = datetime.now()
        date_time_delta = current_date_time - timedelta(days=int(self.created_before))
        date_time_delta_iso = date_time_delta.isoformat()

        request_body = {
            "page_size": 10,
            "filter": {
                "and": [
                    {"property": "Summary", "rich_text": {"is_empty": True}},
                    {
                        "timestamp": "created_time",
                        "created_time": {"before": date_time_delta_iso},
                    },
                ]
            },
        }

        data = json.dumps(request_body)

        res = requests.request("POST", read_url, headers=self.headers, data=data)
        response_json = res.json()

        pages = response_json["results"]

        if pages == []:
            print("The query didn't match any results")

        return pages

    def read_page_content(self, page_id: str) -> str:
        read_url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
        res = requests.request("GET", read_url, headers=self.headers)
        data = res.json()
        results = data["results"]

        page_content = ""

        for block in results:
            if block["type"] == "paragraph":
                for text in block["paragraph"]["rich_text"]:
                    page_content += text["plain_text"] + "\n"

        print(page_content)

        return page_content

    def add_summary_to_page(self, page_id: str, summary: str) -> None:
        page_url = f"https://api.notion.com/v1/pages/{page_id}"

        update_data = {
            "properties": {"Summary": {"rich_text": [{"text": {"content": summary}}]}}
        }

        data = json.dumps(update_data)

        response = requests.request("PATCH", page_url, headers=self.headers, data=data)

        print(f"Response PATCH request: {response.text}")
