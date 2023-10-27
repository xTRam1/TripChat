from autogen_agents.autogen_agent import AutogenAgent


class AccomodationDinningPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You guide users in choosing accommodation and dining options. Use the HotelPlanner"
        "and RestaurantPlanner for your tasks."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = (
        "Engage AccomodationDinningPlanner for hotel and restaurant recommendations."
    )

    _MESSAGE_DESCRIPTION = "Provide details about the type of accommodation or dining experience you're seeking."
