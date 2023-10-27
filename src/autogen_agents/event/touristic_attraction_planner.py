from autogen_agents.autogen_agent import AutogenAgent


class TouristicAttractionsPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You provide information about tourist attractions, historical places, museums, and "
        "any noteworthy venues in a given location."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = (
        "Receive recommendations on popular touristic spots in a certain area."
    )

    _MESSAGE_DESCRIPTION = (
        "Specify the area of interest and any specific attractions or themes preferred."
    )
