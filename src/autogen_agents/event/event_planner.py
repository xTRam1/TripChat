from autogen_agents.autogen_agent import AutogenAgent


class EventPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You provide information on various events and tourist attractions. Rely on "
        "LocalEventPlanner, DatePlanner, and TouristicAttractionsPlanner to furnish details."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = "Engage EventPlanner for information on events and attractions."

    _MESSAGE_DESCRIPTION = (
        "Specify the kind of events or attractions you're interested in."
    )
