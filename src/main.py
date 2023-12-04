import json
import os

from autogen.agentchat.groupchat import GroupChat, GroupChatManager

from autogen_agents import (
    config_list,
    initialize_brain,
    initialize_team_event_planning,
    initialize_team_information,
    initialize_team_logistics,
    initialize_termination_user_proxy,
)
from bookingcom_client import BookingComClient
from custom_groupchat import CUSTOM_GROUP_CHAT_SYSTEM_MESSAGE
from langchain_tool_agents import (
    initialize_bookingcom_agent,
    initialize_search_agent,
    initialize_wikipedia_agent,
)
from plan import plan_template


def main():
    if not os.path.exists("keys.json"):
        raise FileNotFoundError(
            "The 'keys.json' file does not exist. Please create the file with the appropriate keys."
        )

    # Extract keys - "OPENAI_API_KEY", "SERP_API_KEY", "RAPID_API_HOST", and "RAPID_API_KEY"
    keys = {}
    with open("keys.json", "r") as f:
        keys = json.load(f)
    openai_api_key = keys["OPENAI_API_KEY"]
    serp_api_key = keys["SERP_API_KEY"]
    rapid_api_host = keys["RAPID_API_HOST"]
    rapid_api_key = keys["RAPID_API_KEY"]

    user_input = input(
        "What kind of a trip plan do you want? Be as specific as possible (dates, from/to information etc.): "
    )

    # Initialize LangChain Tools and Agents
    os.environ["OPENAI_API_KEY"] = openai_api_key
    bookingcom_client = BookingComClient(
        rapid_api_host=rapid_api_host, rapid_api_key=rapid_api_key
    )
    web_search_agent = initialize_search_agent(serp_api_key=serp_api_key)
    wikipedia_agent = initialize_wikipedia_agent()
    bookingcom_agent = initialize_bookingcom_agent(bookingcom_client=bookingcom_client)
    web_search_function = {"webSearch": web_search_agent.run}
    wikipedia_function = {"Wikipedia": wikipedia_agent.run}
    flight_car_search_function = {"flightOrCarRentalSearch": bookingcom_agent.run}

    # Initialize Autogen Agents
    team_event_planning = initialize_team_event_planning(
        web_search_function, wikipedia_function
    )
    team_logistics = initialize_team_logistics(
        web_search_function, flight_car_search_function
    )
    team_information = initialize_team_information(
        web_search_function, wikipedia_function
    )
    brain = initialize_brain()
    termination_user_proxy = initialize_termination_user_proxy()

    # Initialize GroupChatManager
    list_of_agents = team_event_planning + team_logistics + team_information + [brain]
    group_chat = GroupChat(
        agents=list_of_agents,  # type: ignore
        messages=CUSTOM_GROUP_CHAT_SYSTEM_MESSAGE,
        max_round=10,
    )
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={"config_list": config_list, "cache_seed": None},
    )

    # Start the chat
    try:
        brain.initiate_chat(manager, message=user_input)
    finally:
        bookingcom_client.close()
        print(json.dumps(plan_template, indent=4))


if __name__ == "__main__":
    main()
