from autogen_agents.autogen_agent import AutogenAgent


class LongDistanceTransportationPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You are in charge of planning long-distance travels. Provide options like flights, "
        "trains, or long-drive routes."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = (
        "Seek recommendations or details on long-distance transportation options."
    )

    _MESSAGE_DESCRIPTION = (
        "Provide context, destination, and preferred mode of transportation if any."
    )
