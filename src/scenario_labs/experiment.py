import argparse
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
import xai_sdk

from google import genai

import scenario_labs


GLOBAL_PROVIDER_KEYS = {"xai": "XAI_API_KEY", "google": "GEMINI_API_KEY"}


def get_api_handle(provider: str) -> Any:
    """
    Returns the API client handle based on the provider.

    Args:
        provider (str): The name of the provider (e.g., 'xai', 'google').

    Returns:
        Client class
    """
    api_key = os.getenv(GLOBAL_PROVIDER_KEYS[provider], None)

    if provider not in GLOBAL_PROVIDER_KEYS:
        print(
            f"[Error] Unsupported provider '{provider}'. Supported providers: {', '.join(GLOBAL_PROVIDER_KEYS.keys())}."
        )
        raise ValueError(f"Unsupported provider: {provider}")

    if api_key is None:
        print(
            f"[Error] API key for provider '{provider}' is not set. Please set the environment variable '{GLOBAL_PROVIDER_KEYS[provider]}'."
        )
        raise ValueError(f"API key is not set for provider: {provider}")

    if provider == "xai":
        client = xai_sdk.Client(api_key=api_key)
    elif provider == "google":
        client = genai.Client(api_key=api_key)

    return client


def get_session_handle(provider: str, model: str) -> Any:
    """
    Returns the session handle based on the provider and model.

    Args:
        provider (str): The name of the provider (e.g., 'xai', 'google').
        model (str): The name of the model to use.

    Returns:
        Session handle for the specified provider and model.
    """
    api_handler = get_api_handle(provider)

    # TODO - How widely used is the OpenAI standard?
    #        https://ai.google.dev/gemini-api/docs/openai
    #      - Google chat API
    #        https://github.com/googleapis/python-genai?tab=readme-ov-file#send-message-synchronous-non-streaming
    if provider == "xai":
        session = api_handler.chat.create(model=model)
    elif provider == "google":
        session = api_handler.chats.create(model=model)

    return session


def run_simulation(simulation_config: Dict[str, Any]):
    """
    Runs the LLM-based Conversational Simulation using the provided configuration file.

    Args:
        simulation_config (Dict[str, Any]): The configuration dictionary containing simulation parameters.
    """
    agents = {}
    simulation_name = simulation_config["name"]
    max_turns = simulation_config["max_turns"]
    log_directory = simulation_config["log_directory"]

    for agent in simulation_config.get("agents", []):
        if "id" not in agent or "role" not in agent:
            print("[Warning] Skipping agent with missing 'id' or 'role'.")
            continue

        model = simulation_config.get("model", "grok-3").strip().lower()
        provider = simulation_config.get("provider", "xai").strip().lower()

        session_handle = get_session_handle(provider, model)

        # TODO - Find a common way to append and chat with the agent.
        #        *** See agents/LLMAgent.py for more details. ***
        #        handle them seperately in the agents module. (I like this one)
        # TODO - Works for Google, not for xAI - error:
        # AttributeError: property 'messages' of 'Chat' object has no setter
        # session_handle.messages = [xai_sdk.chat.system(initial_prompt)]

        # TODO - Works for xAI, not for Google - error:
        # AttributeError: 'Chat' object has no attribute 'append'
        # session_handle.append(xai_sdk.chat.system(initial_prompt))

        agents[agent["id"]] = scenario_labs.agents.LLMAgent.LLMAgent(
            agent_id=agent["id"],
            role=agent["role"],
            system_prompt=simulation_config.get("system_prompt", ""),
            initial_prompt=agent["initial_prompt"],
            session=session_handle,
        )

        print(f"[Info] Agent created: {agent['id']} ({agent['role']})")

    if not agents:
        raise ValueError(
            "[Error] No valid agents found in the configuration. Please check the 'agents' section."
        )

    # TODO - Remove, bypass for linting errors.
    print(agents)
    print(simulation_name)
    print(max_turns)
    print(log_directory)

    # simulation = scenario_labs.simulations.conversation.ConversationSimulation(simulation_name, agents, max_turns=max_turns)
    # return simulation.run()


def main():
    parser = argparse.ArgumentParser(
        description="Run the LLM-based Conversational Simulation."
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path("starbound_config.yaml"),
        help="Path to the simulation configuration YAML file (default: starbound_config.yaml)",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    config_text = config_path.read_text(encoding="utf-8")
    config_data = yaml.safe_load(config_text)

    return run_simulation(config_data["simulation_config"])


if __name__ == "__main__":
    main()
