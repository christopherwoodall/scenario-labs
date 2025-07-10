import os
import pytest
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from scenario_labs import experiment

TEMPLATE_DIR = "tests/templates"

def render_config(context):
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["yaml"])
    )
    template = env.get_template("starbound_config.yaml.j2")
    rendered_yaml = template.render(context)
    return yaml.safe_load(rendered_yaml)["simulation_config"]

@pytest.mark.parametrize("provider,model", [
    ("xai", "grok-3"),
    ("openai", "gpt-4o"),
])
def test_run_simulation_does_not_crash(provider, model):
    print(f"\n[RUNNING TEST] provider={provider}, model={model}")

    config = render_config({
        "simulation_name": f"Test run - {provider}",
        "max_turns": 2,
        "model": model,
        "provider": provider,
        "log_directory": f"./logs/test_run_simulation/{provider}",
        "agents": [
            {
                "id": "TestBot1",
                "role": "Mock Role A",
                "initial_prompt": "Say hi from TestBot1",
            },
            {
                "id": "TestBot2",
                "role": "Mock Role B",
                "initial_prompt": "Say hi from TestBot2",
            },
        ],
    })

    result = experiment.run_simulation(config)

    print(f"[COMPLETE] provider={provider}, model={model}")
    print(f"[RESULT] {result}")
