from autogen_agents.autogen_agent import AutogenAgent


class TravelPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You are the TravelPlanner. You assist with long-distance and short-distance "
        "transportation and help decide stops during the journey. Use LongDistanceTransportationPlanner, "
        "ShortDistanceTransportationPlanner, and StopPlanner to offer the best travel options."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = "Engage TravelPlanner to assist with both long-distance and short-distance travel options."

    _MESSAGE_DESCRIPTION = "Inquiry for TravelPlanner, specify if you're looking for long/short distance options or specific stops."
