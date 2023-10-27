from autogen_agents.autogen_agent import AutogenAgent


class WeatherAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You provide up-to-date weather information for any given location."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "information"}

    _DESCRIPTION = "Offer weather forecasts or current weather conditions for a specified location."

    _MESSAGE_DESCRIPTION = (
        "Specify the location and whether you need a current report or forecast."
    )
