from typing import Any, Dict, List
from google import genai

from scenario_labs.client.base import ChatClient


class GoogleGenAIClient(ChatClient):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = self.client.chats.create(model=model)
        self.history = []

        from pprint import pprint

        print(f"{self.__class__.__name__} state:")
        pprint(vars(self), sort_dicts=False)


    def chat(self,
             messages: List[Dict[str, str]],
             temperature: float = 0.7,
             **kwargs) -> Dict[str, Any]:
        # google.genai expects a list of dicts with "author" instead of "role"
        g_messages = []
        for msg in messages:
            author = "user" if msg["role"] == "user" else "bot" if msg["role"] == "assistant" else "system"
            g_messages.append({"author": author, "content": msg["content"]})

        response = self.client.send(
            model=self.model,
            temperature=temperature,
            messages=g_messages,
            **kwargs
        )
        return response


# def get_session_handle(provider: str, model: str) -> Any:
#     """
#     Returns the session handle based on the provider and model.

#     Args:
#         provider (str): The name of the provider (e.g., 'xai', 'google').
#         model (str): The name of the model to use.

#     Returns:
#         Session handle for the specified provider and model.
#     """
#     api_handler = get_api_handle(provider)

#     # TODO - How widely used is the OpenAI standard?
#     #        https://ai.google.dev/gemini-api/docs/openai
#     #      - Google chat API
#     #        https://github.com/googleapis/python-genai?tab=readme-ov-file#send-message-synchronous-non-streaming
#     if provider == "xai":
#         session = api_handler.chat.create(model=model)
#     elif provider == "google":
#         session = api_handler.chats.create(model=model)

#     return session


# TODO - Find a common way to append and chat with the agent
#        handle them seperately in the agents module. (I like this one)
# TODO - Works for Google, not for xAI - error:
# AttributeError: property 'messages' of 'Chat' object has no setter
# session_handle.messages = [xai_sdk.chat.system(initial_prompt)]

# TODO - Works for xAI, not for Google - error:
# AttributeError: 'Chat' object has no attribute 'append'
# session_handle.append(xai_sdk.chat.system(initial_prompt))

# Initialize the session with the system prompt
# self.session.append(user(f"Agent {self.agent_id} ({self.role}) is thinking..."))
# response = self.session.sample()
# self.session.append(response)

