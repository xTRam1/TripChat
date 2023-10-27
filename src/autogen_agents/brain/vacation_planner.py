from autogen_agents.autogen_agent import AutogenAgent


class VacationPlannerAgent(AutogenAgent):
    _SYSTEM_MESSAGE = (
        "You are the VacationPlanner. Your role is to assist with planning vacations. You "
        "use the services of TravelPlanner, AccomodationDinningPlanner, EventPlanner, and InformationServices "
        "to provide comprehensive vacation planning."
    )

    _CODE_EXECUTION_CONFIG = {"work_dir": "planning"}

    _DESCRIPTION = (
        "Request VacationPlanner to assist with planning vacations, consolidating "
        "details from its various sub-agents."
    )

    _MESSAGE_DESCRIPTION = (
        "Question for VacationPlanner. Ensure the question has enough context about user's vacation needs. "
        "The sub-agent does not have previous knowledge of the conversation."
    )
