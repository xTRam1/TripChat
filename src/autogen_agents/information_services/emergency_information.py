from autogen_agents.autogen_agent import AutogenAgent


class EmergencyInformationAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You provide emergency contact details, helpline numbers, and any other vital "
        "information required during emergencies."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "information"}

    _DESCRIPTION = (
        "Provide emergency contact details or information for a given location."
    )

    _MESSAGE_DESCRIPTION = "Specify the location for which you need emergency contact details or related information."
