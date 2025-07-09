import argparse
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from xai_sdk import Client
from xai_sdk.chat import system

from google import genai

from agents.LLMAgent import LLMAgent
from simulations.conversation import ConversationSimulation


GLOBAL_PROVIDER_KEYS = {"xai": "XAI_API_KEY", "google": "GOOGLE_API_KEY"}


def read_config(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Reads a YAML configuration file and returns its content as a dictionary.

    Args:
        file_path (Path): The path to the YAML configuration file.

    Returns:
        Optional[Dict[str, Any]]: Parsed configuration dictionary, or None if the file is missing or invalid.
    """
    if not file_path.exists():
        print(f"[Error] Configuration file '{file_path}' does not exist.")
        return None

    with file_path.open("r") as file:
        return yaml.safe_load(file)


def get_api_handle(provider: str, model: str):
    """
    Returns the API key environment variable name based on the provider.

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
        print(f"[Error] API key for provider '{provider}' is not set. Please set the environment variable '{GLOBAL_PROVIDER_KEYS[provider]}'.")
        raise ValueError(f"API key is not set for provider: {provider}")

    if provider == "xai":
        client = Client(api_key=api_key)
    elif provider == "google":
        client = genai.Client(api_key=api_key)

    return client


def run_simulation(config_path: Path):
    """
    Runs the LLM-based Conversational Simulation using the provided configuration file.

    Args:
        config_path (Path): Path to the simulation configuration YAML file.
    """
    config = read_config(config_path)
    simulation_config = config["simulation_config"]

    agents = {}
    simulation_name = simulation_config["name"]
    max_turns = simulation_config["max_turns"]

    for agent in simulation_config.get("agents", []):
        if "id" not in agent or "role" not in agent:
            print("[Warning] Skipping agent with missing 'id' or 'role'.")
            continue

        initial_prompt = "\n".join(
            [simulation_config.get("system_prompt", ""), agent["initial_prompt"]]
        )

        # NEW
        provider = simulation_config.get("provider", "xai").strip().lower()
        model = simulation_config.get("model", "grok-3").strip().lower()
        
        client = get_api_handle(provider, model)
        # TODO - Harmonize the session creation for different providers
        #      - Chat works different for xai and google, need to handle both
        #        https://github.com/googleapis/python-genai?tab=readme-ov-file#system-instructions-and-other-configs
        #      - Can we use the OpenAI standard for both?
        #        https://ai.google.dev/gemini-api/docs/openai
        #
        # session = client.chat.create(
        #     model=model,
        #     messages=[system(initial_prompt)],
        # )
        # 
        # session = client.chat.completions.create()
        # /NEW

        agents[agent["id"]] = LLMAgent(
            agent_id=agent["id"],
            role=agent["role"],
            initial_prompt=agent["initial_prompt"],
            # session=session,
        )

        print(f"[Info] Agent created: {agent['id']} ({agent['role']})")

    # simulation = ConversationSimulation(simulation_name, agents, max_turns=max_turns)
    # simulation.run()


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
    run_simulation(args.config)


if __name__ == "__main__":
    main()
