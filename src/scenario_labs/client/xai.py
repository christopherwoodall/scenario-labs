from typing import Any, Dict, List

import xai_sdk

from scenario_labs.client.base import ChatClient


class xAIChatClient(ChatClient):
    def __init__(self, api_key: str, model: str = "grok-3"):
        self.client = xai_sdk.Client(api_key=api_key)
        self.model = self.client.chat.create(model=model)

    def chat(
        self, messages: List[Dict[str, str]], temperature: float = 0.7, **kwargs
    ) -> Dict[str, Any]:
        # xai_sdk expects a list of strings or some structured payload
        # adapt your messages format if needed
        response = self.client.chat(
            model=self.model, messages=messages, temperature=temperature, **kwargs
        )
        return response
