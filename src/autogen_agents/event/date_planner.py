from autogen_agents.autogen_agent import AutogenAgent


class DatePlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You suggest ideas and places for dates. This includes romantic venues, activities, "
        "or any special events happening locally."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = "Get ideas or plans for date activities in a given locale."

    _MESSAGE_DESCRIPTION = (
        "Specify the locale, any interests, and special requirements."
    )
