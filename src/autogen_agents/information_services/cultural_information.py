from autogen_agents.autogen_agent import AutogenAgent


class CulturalInformationAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You offer cultural insights, dos and don'ts, and any other relevant cultural "
        "details about a particular location or event."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "information"}

    _DESCRIPTION = "Provide insights or details about the culture of a specific region or locality."

    _MESSAGE_DESCRIPTION = (
        "Mention the region or locality of interest for cultural insights."
    )
