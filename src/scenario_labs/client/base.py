from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ChatClient(ABC):
    model: str
    client: str

    @abstractmethod
    def chat(
        self, messages: List[Dict[str, str]], temperature: float = 0.7, **kwargs
    ) -> Dict[str, Any]: ...


# TODO - How widely used is the OpenAI standard?
#        https://ai.google.dev/gemini-api/docs/openai
#      - Google chat API
#        https://github.com/googleapis/python-genai?tab=readme-ov-file#send-message-synchronous-non-streaming
