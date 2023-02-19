import openai
import re


class OpenAIRequest:
    def __init__(self, token: str) -> None:
        self.token = token

    def get_summary(self, text: str) -> str:
        """
        Query the OpenAI end-point using the 'tl;dr' prompt and clean the end-result to one string.
        """
        openai.api_key = self.token

        body = text + "\n\n Tl;dr"

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=body,
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        result = ""

        for content in response["choices"]:
            result += content["text"]

        clean_result = result.replace("\n", " ").replace("\r", "").lstrip()

        result_without_colon = re.sub(r"^\W+", "", clean_result)

        print(f"Summary result: {result_without_colon}")

        return result_without_colon
