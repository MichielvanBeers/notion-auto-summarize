import requests
import json


class OpenAIRequest:
    def __init__(self, token: str, model: str) -> None:
        self.token = token
        self.model = model

    def get_summary(self, prompt: str) -> str:
        """
        Query the OpenAI end-point
        """
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        body = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": """You are a summarizer. For every input you receive, 
                    you return the summary in maximum 400 characters""",
                },
                {"role": "user", "content": prompt},
            ],
        }

        data = json.dumps(body)

        response = requests.request("POST", url, headers=headers, data=data)

        result = ""
        response_json = response.json()
        if response.ok:
            for entry in response_json["choices"]:
                result += entry["message"]["content"]
        else:
            print(f"API returned {response.status_code} with message: {response_json}")

        return result
