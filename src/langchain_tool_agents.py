from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.tools import StructuredTool, Tool, WikipediaQueryRun
from langchain.utilities import SerpAPIWrapper, WikipediaAPIWrapper
from pydantic import BaseModel

from bookingcom_client import BookingComClient
from config import MAX_TOKENS, MODEL_NAME, TEMPERATURE

SERP_API_KEY = "<YOUR_SERP_API_KEY>"


class WebSearch(BaseModel):
    input: str


def initialize_search_agent() -> AgentExecutor:
    serp_api_wrapper = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)  # type: ignore
    web_search_llm = ChatOpenAI(
        model=MODEL_NAME,
        client=None,
        temperature=TEMPERATURE,
        streaming=False,
        max_tokens=MAX_TOKENS,
    )
    tools = [
        Tool(
            name="webSearch",
            description="Tool for searching queries from google.com"
            "Input is a string",
            args_schema=WebSearch,
            func=serp_api_wrapper.run,
        )
    ]

    # Web Search Memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    web_search_agent_system_message = (
        "You will be given a user query and you MUST call the webSearch tool to "
    )
    "get back search results from google.com and provide a concise answer back to the user. You are only allowed to call the tools "
    "at most three times or less."
    memory.chat_memory.add_message(
        SystemMessage(
            content=web_search_agent_system_message,
        )
    )

    # Agent
    web_search_agent = initialize_agent(
        tools,
        web_search_llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=True,
    )

    return web_search_agent


def initialize_wikipedia_agent() -> AgentExecutor:
    # Tool setup
    wikipedia_llm = ChatOpenAI(
        model=MODEL_NAME,
        client=None,
        temperature=TEMPERATURE,
        streaming=False,
        max_tokens=MAX_TOKENS,
    )
    tools = [WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())]

    # Wikipedia Memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    wikipedia_agent_system_message = (
        "You will be given a user query and you MUST call the Wikipedia tool to "
    )
    "get back search results from Wikipedia and provide a concise answer back to the user. You are only allowed to call the tools "
    "at most three times or less."
    memory.chat_memory.add_message(
        SystemMessage(
            content=wikipedia_agent_system_message,
        )
    )

    # Agent
    wikipedia_agent = initialize_agent(
        tools,
        wikipedia_llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=True,
    )

    return wikipedia_agent


class FlightSearch(BaseModel):
    departure_location: str
    arrival_location: str
    departure_date: str


class CarRentalSearch(BaseModel):
    location_query: str
    pick_up_date: str
    drop_off_date: str
    pick_up_time: str
    drop_off_time: str


def initialize_bookingcom_agent(bookingcom_client: BookingComClient) -> AgentExecutor:
    # Tool setup
    bookingcom_llm = ChatOpenAI(
        model=MODEL_NAME,
        client=None,
        temperature=TEMPERATURE,
        streaming=False,
        max_tokens=MAX_TOKENS,
    )
    tools = [
        StructuredTool(
            name="flightsSearch",
            description="Tool for searching flights from booking.com"
            "departure_location is a string"
            "arrival_location is a string"
            "departure_date is a string in the format YYYY-MM-DD",
            args_schema=FlightSearch,
            func=bookingcom_client.flights_search_tool,
        ),
        StructuredTool(
            name="carRentalSearch",
            description="Tool for searching car rentals from booking.com"
            "location_query is the location in which you are searching a car rental and is a string"
            "pick_up_date is a string in the format YYYY-MM-DD"
            "drop_off_date is a string in the format YYYY-MM-DD"
            "pick_up_time is a time and is a string in the format HH:MM"
            "drop_off_time is a time is a string in the format HH:MM",
            args_schema=CarRentalSearch,
            func=bookingcom_client.car_rental_search_tool,
        ),
    ]

    # Booking.com Memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    bookingcom_agent_system_message = "You will be given a user query and you MUST call the flightsSearch or carRentalSearch tool to "
    "get back search results from booking.com and provide the results from the tools directly back to the user without modification. "
    "You MUST only make one function call and only use one tool. You are only allowed to call the tools. If you are not given "
    "sufficient information to make a booking, you MUST make a reasonable choice yourself. "
    memory.chat_memory.add_message(
        SystemMessage(
            content=bookingcom_agent_system_message,
        )
    )

    # Agent
    bookingcom_agent = initialize_agent(
        tools,
        bookingcom_llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=True,
    )

    return bookingcom_agent


# Schemas
web_search_agent_func_schema = {
    "name": "webSearch",
    "description": "Tool for searching queries from google.com.",
    "parameters": {
        "type": "object",
        "properties": {
            "input": {"type": "string", "description": "The query to search for."},
        },
        "required": ["input"],
    },
}

wikipedia_agent_func_schema = {
    "name": "Wikipedia",
    "description": "Tool for searching queries from wikipedia.com.",
    "parameters": {
        "type": "object",
        "properties": {
            "input": {"type": "string", "description": "The query to search for."},
        },
        "required": ["input"],
    },
}

flight_car_search_agent_func_schema = {
    "name": "flightOrCarRentalSearch",
    "description": "Tool for searching flight and car rental information from booking.com.",
    "parameters": {
        "type": "object",
        "properties": {
            "input": {
                "type": "string",
                "description": "The query to search for. Must either be about a flight or a car rental and not both.",
            },
        },
        "required": ["input"],
    },
}