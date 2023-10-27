from autogen_agents.autogen_agent import AutogenAgent


class LocalPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You are the LocalPlanner. Your role is to suggest local events and attractions. "
        "Collaborate with the TravelPlanner, AccomodationDinningPlanner, EventPlanner, "
        "and InformationServices to provide the best recommendations."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = (
        "Ask LocalPlanner for information about local events and attractions."
    )

    _MESSAGE_DESCRIPTION = (
        "Question for LocalPlanner regarding specific events or local attractions."
        "Provide necessary context for clarity."
    )
