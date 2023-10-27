from typing import Any

from langchain.agents import load_tools
from langchain.tools import BaseTool, GooglePlacesTool, Tool
from pydantic import BaseModel, Field


class GoogleSearchInput(BaseModel):
    query: str = Field()


def init_custom_google_search_tools(
    google_search_wrapper: Any, name: str, description: str
) -> Tool:
    return Tool.from_function(
        func=google_search_wrapper.run,
        name=name,
        description=description,
        args_schema=GoogleSearchInput,  # type: ignore
    )


def init_google_places_tools() -> Tool:
    return GooglePlacesTool()


def init_open_weather_map_tools() -> list[BaseTool]:
    return load_tools(["openweathermap-api"])


def init_wikipedia_tools() -> list[BaseTool]:
    return load_tools(["wikipedia"])
