from typing import Any, Dict

import scenario_labs


class OneShotSimulation:
    """
    Class to handle one-shot simulations (evaluation).
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.evaluation_log = {
            "model": config.get("model", "grok-3").strip().lower(),
            "provider": config.get("provider", "xai").strip().lower(),
            "system_prompt": config.get("system_prompt", ""),
            "simulation_name": config.get("name", "one_shot_simulation"),
            "log_directory": config.get("log_directory", "logs/one_shot"),
            "responses": [],
        }

    def run(self):
        """
        Run the one-shot simulation based on the provided configuration.
        """
        agent = self.config["agents"][0]
        agent_prompts = agent["prompts"]

        for prompt in agent_prompts:
            model = agent.get("model", self.evaluation_log["model"])
            provider = agent.get("provider", self.evaluation_log["provider"])

            session = scenario_labs.client.factory.get_chat_client(
                provider=provider,
                model=model,
            )
            session.initialize(self.evaluation_log["system_prompt"])

            response = session.chat(prompt)

            self.evaluation_log["responses"].append({
                "system": self.evaluation_log["system_prompt"],
                "user": prompt,
                "assistant": response
            })

        # TODO - Implement logging to file
        # self.evaluation_log["log_file"] = self._save_log_to_file()

        print("[Info] One-shot simulation completed.")

        return self.evaluation_log
    