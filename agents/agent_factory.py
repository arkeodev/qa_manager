# agents/agent_factory.py

"""Factory for creating agents."""

import json
import logging
from typing import Any, Dict

from autogen import AssistantAgent, UserProxyAgent


class AgentFactory:
    """Factory class to create agents based on configurations."""

    @staticmethod
    def create_agent(agent_config: Dict[str, Any], llm_config: Dict[str, Any]) -> Any:
        """
        Create an agent based on the provided configuration.

        Args:
            agent_config (Dict[str, Any]): The configuration for the agent.
            llm_config (Dict[str, Any]): The LLM configuration.

        Returns:
            Any: An instance of the agent.
        """
        agent_type = agent_config.get('agent_type')
        logging.info(f"Creating agent of type: {agent_type}")

        agent_classes = {
            "AssistantAgent": AssistantAgent,
            "UserProxyAgent": UserProxyAgent,
        }

        if agent_type not in agent_classes:
            raise ValueError(f"Unknown agent type: {agent_type}")

        agent_class = agent_classes[agent_type]
        agent = agent_class(
            name=agent_config['name'],
            system_message=agent_config['system_message'],
            description=agent_config.get('description', ''),
            llm_config=llm_config,
            human_input_mode=agent_config.get('human_input_mode', 'NEVER'),
            max_consecutive_auto_reply=agent_config.get('max_consecutive_auto_reply', 5),
        )
        return agent


def load_agent_configs(config_file: str = 'configs/agent_config.json') -> Dict[str, Any]:
    """
    Load agent configurations from a JSON file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        Dict[str, Any]: Agent configurations.
    """
    logging.info("Loading agent configurations")
    with open(config_file, "r") as f:
        return json.load(f)


def create_agents(llm_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create agents based on configurations and LLM settings.

    Args:
        llm_config (Dict[str, Any]): The LLM configuration.

    Returns:
        Dict[str, Any]: A dictionary of agent instances.
    """
    logging.info(f"Creating agents with llm_config: {llm_config}")

    agent_configs = load_agent_configs()
    agents = {}
    for agent_name, agent_config in agent_configs.items():
        logging.info(f"Creating agent: {agent_name}")
        agents[agent_name] = AgentFactory.create_agent(agent_config, llm_config)
    return agents
