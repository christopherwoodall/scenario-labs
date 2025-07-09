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


def run_simulation(config_path: Path):
    """
    Runs the LLM-based Conversational Simulation using the provided configuration file.

    Args:
        config_path (Path): Path to the simulation configuration YAML file.
    """
    config = read_config(config_path)
    simulation_config = config["simulation_config"]

    ## NEW
    env_keys = {
        "xai": "XAI_API_KEY",
        "google": "GOOGLE_API_KEY"
    }
    
    provider = simulation_config.get("provider", "xai")
    model = simulation_config.get("model", "grok-3")

    api_key = os.getenv(env_keys[provider])

    client = Client(api_key=api_key)
    # client = genai.Client() # Google GenAI client

    # TODO - Determine the provider in order to use the correct client
    ## /NEW

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
        session = client.chat.create(
            model="grok-3",
            messages=[system(initial_prompt)],
        )

        agents[agent["id"]] = LLMAgent(
            agent_id=agent["id"],
            role=agent["role"],
            initial_prompt=agent["initial_prompt"],
            session=session,
        )

        print(f"[Info] Agent created: {agent['id']} ({agent['role']})")

    simulation = ConversationSimulation(simulation_name, agents, max_turns=max_turns)
    simulation.run()


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
