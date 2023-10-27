from autogen_agents.autogen_agent import AutogenAgent


class HotelPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = "You help users find suitable hotels based on their preferences, budget, and travel dates."

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = "Get recommendations or details for hotels in a given location."

    _MESSAGE_DESCRIPTION = (
        "Specify location, date range, budget, and any other preferences for hotels."
    )
