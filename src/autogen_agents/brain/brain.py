from autogen_agents.autogen_agent import AutogenAgent


class BrainAgent(AutogenAgent):
    _SYSTEM_MESSAGE = "You are the BrainAssistant, the primary AI interface. You orchestrate between the VacationPlanner "
    "and LocalPlanner. Ensure you gather and consolidate information from these sub-agents to provide a comprehensive "
    "response to the user's request."

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    def run(self, message: str, parallel: bool = False) -> None:
        self._user_proxy_agent.initiate_chat(self._assistant_agent, message=message)
