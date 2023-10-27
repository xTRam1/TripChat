from autogen_agents.autogen_agent import AutogenAgent


class StopPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = "You suggest stops during a journey, be it for rest, sightseeing, gas station, or any other necessities."

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = "Plan specific stops or waypoints during a journey."

    _MESSAGE_DESCRIPTION = "Outline the journey's start, end, and any preferences or constraints for stops."
