from autogen_agents.autogen_agent import AutogenAgent


class LocalEventPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You provide information about local events, festivals, and other activities happening "
        "in a given location."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = (
        "Engage the LocalEventPlanner for events and attractions in a specific region."
    )

    _MESSAGE_DESCRIPTION = "Provide context or specific queries regarding events or attractions in the desired region."
