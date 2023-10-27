from autogen_agents.autogen_agent import AutogenAgent


class ShortDistanceTransportationPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You assist with short-distance transportation options. This includes local buses, trams, "
        "taxis, or walking routes."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = "Seek recommendations or details on short-distance transportation within a locality."

    _MESSAGE_DESCRIPTION = (
        "Specify the locality, points of interest, and any preferences."
    )
