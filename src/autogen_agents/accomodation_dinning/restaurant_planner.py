from autogen_agents.autogen_agent import AutogenAgent


class RestaurantPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You assist users in finding restaurants, cafes, or any other dining options based on "
        "their preferences and location."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = "Get dining recommendations or details within a certain area."

    _MESSAGE_DESCRIPTION = (
        "Specify location, cuisine preference, budget, and any special requirements."
    )
