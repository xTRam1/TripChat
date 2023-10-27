from abc import ABC
from typing import Any, TypedDict, Unpack

from autogen import AssistantAgent, UserProxyAgent


class AutogenConstants:
    # TODO: Tweak these, don't know what they actually do
    HUMAN_INPUT_MODE = "NEVER"
    MAX_CONSECUTIVE_AUTO_REPLY = 1
    IS_TERMINATION_MSG = (
        lambda x: "content" in x
        and x["content"] is not None
        and x["content"].rstrip().endswith("TERMINATE")
    )
    LLM_CONFIG_CONSTANTS = {
        "temperature": 0,
        "request_timeout": 600,
        # "seed": 42, # Add this if you want to test agents deterministically
    }


class AutogenAgentInitParams(TypedDict):
    name: str
    model: str
    children_agents: list[
        "AutogenAgent"
    ]  # TODO: Add the LangchainAgent class next to a | operator when they are implemented
    config_list: list[dict[str, Any]]


class AutogenAgent(ABC):
    # Initialization parameters
    name: str
    model: str
    children_agents: list["AutogenAgent"]
    config_list: list[dict[str, Any]]

    # Private Fields - Calculated
    _assistant_agent: AssistantAgent
    _user_proxy_agent: UserProxyAgent
    _function_map: dict[str, Any]
    _llm_config: dict[str, Any]

    # Constants
    _SYSTEM_MESSAGE: str
    # TODO: I don't know what _CODE_EXECUTION_CONFIG is
    _CODE_EXECUTION_CONFIG: dict[str, Any]
    _DESCRIPTION: str
    _MESSAGE_DESCRIPTION: str

    def __init__(self, **kwargs: Unpack[AutogenAgentInitParams]) -> None:
        # Init Parameters
        self.name = kwargs["name"]
        self.model = kwargs["model"]
        self.children_agents = kwargs["children_agents"]
        self.config_list = kwargs["config_list"]

        # Calculated fields
        self._llm_config = {
            **AutogenConstants.LLM_CONFIG_CONSTANTS,
            "model": self.model,
            "functions": [
                {
                    "name": f"ask_{child.name}",
                    "description": child._DESCRIPTION,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": child._MESSAGE_DESCRIPTION,
                            }
                        },
                        "required": ["message"],
                    },
                }
                for child in self.children_agents
            ],
            "config_list": self.config_list,
        }
        self._function_map = {
            f"ask_{child.name}": child.ask_agent for child in self.children_agents
        }
        self._assistant_agent = AssistantAgent(
            name=self.name,
            llm_config=self._llm_config,
            system_message=self._SYSTEM_MESSAGE,
        )
        self._user_proxy_agent = UserProxyAgent(
            name=f"{self.name}_user",
            human_input_mode=AutogenConstants.HUMAN_INPUT_MODE,
            max_consecutive_auto_reply=AutogenConstants.MAX_CONSECUTIVE_AUTO_REPLY,
            is_termination_msg=AutogenConstants.IS_TERMINATION_MSG,
            code_execution_config=self._CODE_EXECUTION_CONFIG,
            function_map=self._function_map,
        )

    def ask_agent(self, message: str) -> Any:
        self._user_proxy_agent.initiate_chat(self._assistant_agent, message=message)
        return self._user_proxy_agent.last_message()["content"]
