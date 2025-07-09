from typing import Any, Dict
from google import genai

from scenario_labs.client.base import ChatClient


class GoogleGenAIClient(ChatClient):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = self.client.chats.create(model=model)

        from pprint import pprint

        print(f"{self.__class__.__name__} state:")
        pprint(vars(self), sort_dicts=False)

    def chat(self, message: str) -> Dict[str, Any]:
        response = self.model.send_message(message)
        return response
