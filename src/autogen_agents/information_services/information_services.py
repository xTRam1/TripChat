from autogen_agents.autogen_agent import AutogenAgent


class InformationServicesAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You offer essential information services like weather, cultural insights, "
        "and emergency contacts. Use Weather, CulturalInformation, and EmergencyInformation for this purpose."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = (
        "Request InformationServices for weather, cultural, or emergency details."
    )

    _MESSAGE_DESCRIPTION = "Specify the information category: weather, cultural details, or emergency contacts."
