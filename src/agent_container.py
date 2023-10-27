from autogen import config_list_from_models
from langchain.utilities import GoogleSearchAPIWrapper

from autogen_agents.accomodation_dinning.accomodation_dinning_planner import (
    AccomodationDinningPlannerAgent,
)
from autogen_agents.accomodation_dinning.hotel_planner import HotelPlannerAgent
from autogen_agents.accomodation_dinning.restaurant_planner import (
    RestaurantPlannerAgent,
)
from autogen_agents.brain.brain import BrainAgent
from autogen_agents.brain.local_planner import LocalPlannerAgent
from autogen_agents.brain.vacation_planner import VacationPlannerAgent
from autogen_agents.event.date_planner import DatePlannerAgent
from autogen_agents.event.event_planner import EventPlannerAgent
from autogen_agents.event.local_event_planner import LocalEventPlannerAgent
from autogen_agents.event.touristic_attraction_planner import (
    TouristicAttractionsPlannerAgent,
)
from autogen_agents.information_services.cultural_information import (
    CulturalInformationAgent,
)
from autogen_agents.information_services.emergency_information import (
    EmergencyInformationAgent,
)
from autogen_agents.information_services.information_services import (
    InformationServicesAgent,
)
from autogen_agents.information_services.weather import WeatherAgent
from autogen_agents.travel.long_distance_transportation_planner import (
    LongDistanceTransportationPlannerAgent,
)
from autogen_agents.travel.short_distance_transportation_planner import (
    ShortDistanceTransportationPlannerAgent,
)
from autogen_agents.travel.stop_planner import StopPlannerAgent
from autogen_agents.travel.travel_planner import TravelPlannerAgent
from config.config import config_model_list
from langchain_agents.langchain_agent import LangchainAgent
from langchain_agents.tools import (
    init_custom_google_search_tools,
    init_google_places_tools,
    init_open_weather_map_tools,
    init_wikipedia_tools,
)


class AgentContainer:
    config_list = config_list_from_models(model_list=config_model_list)

    # LangchainTools: Google search, Google Places, Weather, Wikipedia, etc.
    google_places_tool = init_google_places_tools()
    openweathermap_tools = init_open_weather_map_tools()
    wikipedia_tools = init_wikipedia_tools()
    google_search_wrapper = GoogleSearchAPIWrapper()
    google_restaurant_search_tool = init_custom_google_search_tools(
        google_search_wrapper=google_search_wrapper,
        name="Google Search for restaurants",
        description="Useful for when you need to find restaurants in Google. Try looking for sites like Tripadvisor, Yelp, or Google Maps...",
    )
    google_hotel_search_tool = init_custom_google_search_tools(
        google_search_wrapper=google_search_wrapper,
        name="Google Search for hotels",
        description="Useful for when you need to find hotels in Google. Try looking for sites like Hotels.com, Tripadvisor, or Airbnb...",
    )
    google_event_search_tool = init_custom_google_search_tools(
        google_search_wrapper=google_search_wrapper,
        name="Google Search for events",
        description="Useful for when you need to find events in Google. Try looking for sites like Eventbrite, Stubhub, or Ticketmaster...",
    )
    google_attraction_search_tool = init_custom_google_search_tools(
        google_search_wrapper=google_search_wrapper,
        name="Google Search for attractions",
        description="Useful for when you need to find attractions in Google. Try looking for blogs, tour guides, or travel sites...",
    )
    google_transportation_search_tool = init_custom_google_search_tools(
        google_search_wrapper=google_search_wrapper,
        name="Google Search for transportation",
        description="Useful for when you need to find transportation in Google. Try looking for sites like Google Maps, Rome2Rio, or Uber...",
    )
    google_emergency_search_tool = init_custom_google_search_tools(
        google_search_wrapper=google_search_wrapper,
        name="Google Search for emergencies",
        description="Useful for when you need to find emergency information in Google. Try looking for local news, government sites, or travel sites...",
    )

    # Travel Planner Agents
    langchain_travel_agent = LangchainAgent(
        name="travel_agent",
        model="gpt-3.5-turbo",
        tools=[google_transportation_search_tool],
    )
    long_distance_transportation_planner_agent = LongDistanceTransportationPlannerAgent(
        name="long_distance_transportation_planner",
        model="gpt-3.5-turbo",
        children_agents=[langchain_travel_agent],
        config_list=config_list,
    )
    short_distance_transportation_planner_agent = (
        ShortDistanceTransportationPlannerAgent(
            name="short_distance_transportation_planner",
            model="gpt-3.5-turbo",
            children_agents=[langchain_travel_agent],
            config_list=config_list,
        )
    )
    stop_planner_agent = StopPlannerAgent(
        name="stop_planner",
        model="gpt-3.5-turbo",
        children_agents=[langchain_travel_agent],
        config_list=config_list,
    )
    travel_planner_agent = TravelPlannerAgent(
        name="travel_planner",
        model="gpt-3.5-turbo",
        children_agents=[
            long_distance_transportation_planner_agent,
            short_distance_transportation_planner_agent,
            stop_planner_agent,
        ],
        config_list=config_list,
    )

    # Accomodation Dunning Planner Agents
    lanchain_hotel_agent = LangchainAgent(
        name="hotel_agent",
        model="gpt-3.5-turbo",
        tools=[google_hotel_search_tool],
    )
    lanchain_restaurant_agent = LangchainAgent(
        name="restaurant_agent",
        model="gpt-3.5-turbo",
        tools=[google_restaurant_search_tool],
    )
    hotel_planner_agent = HotelPlannerAgent(
        name="hotel_planner",
        model="gpt-3.5-turbo",
        children_agents=[lanchain_hotel_agent],
        config_list=config_list,
    )
    restaurant_planner_agent = RestaurantPlannerAgent(
        name="restaurant_planner",
        model="gpt-3.5-turbo",
        children_agents=[lanchain_restaurant_agent],
        config_list=config_list,
    )
    accomodation_dinning_planner_agent = AccomodationDinningPlannerAgent(
        name="accomodation_dinning_planner",
        model="gpt-3.5-turbo",
        children_agents=[hotel_planner_agent, restaurant_planner_agent],
        config_list=config_list,
    )

    # Event Planner Agents
    langchain_event_agent = LangchainAgent(
        name="event_agent",
        model="gpt-3.5-turbo",
        tools=[google_event_search_tool],
    )
    langchain_attraction_agent = LangchainAgent(
        name="attraction_agent",
        model="gpt-3.5-turbo",
        tools=[google_attraction_search_tool] + wikipedia_tools,
    )
    local_event_planner_agent = LocalEventPlannerAgent(
        name="local_event_planner",
        model="gpt-3.5-turbo",
        children_agents=[langchain_event_agent],
        config_list=config_list,
    )
    date_planner_agent = DatePlannerAgent(
        name="date_planner",
        model="gpt-3.5-turbo",
        children_agents=[langchain_event_agent],
        config_list=config_list,
    )
    touristic_attractions_planner_agent = TouristicAttractionsPlannerAgent(
        name="touristic_attractions_planner",
        model="gpt-3.5-turbo",
        children_agents=[langchain_attraction_agent],
        config_list=config_list,
    )
    event_planner_agent = EventPlannerAgent(
        name="event_planner",
        model="gpt-3.5-turbo",
        children_agents=[
            local_event_planner_agent,
            date_planner_agent,
            touristic_attractions_planner_agent,
        ],
        config_list=config_list,
    )

    # Information Services Agents
    langchain_weather_agent = LangchainAgent(
        name="weather_agent",
        model="gpt-3.5-turbo",
        tools=openweathermap_tools,
    )
    langchain_cultural_information_agent = LangchainAgent(
        name="cultural_information_agent",
        model="gpt-3.5-turbo",
        tools=wikipedia_tools,
    )
    lanchain_emergency_agent = LangchainAgent(
        name="emergency_agent",
        model="gpt-3.5-turbo",
        tools=[google_emergency_search_tool],
    )
    weather_agent = WeatherAgent(
        name="weather",
        model="gpt-3.5-turbo",
        children_agents=[langchain_weather_agent],
        config_list=config_list,
    )
    cultural_information_agent = CulturalInformationAgent(
        name="cultural_information",
        model="gpt-3.5-turbo",
        children_agents=[langchain_cultural_information_agent],
        config_list=config_list,
    )
    emergency_agent = EmergencyInformationAgent(
        name="emergency",
        model="gpt-3.5-turbo",
        children_agents=[lanchain_emergency_agent],
        config_list=config_list,
    )
    information_services_agent = InformationServicesAgent(
        name="information_services",
        model="gpt-3.5-turbo",
        children_agents=[weather_agent, cultural_information_agent, emergency_agent],
        config_list=config_list,
    )

    # Vacation Planner Agent
    vacation_planner_agent = VacationPlannerAgent(
        name="vacation_planner",
        model="gpt-3.5-turbo",
        children_agents=[
            travel_planner_agent,
            accomodation_dinning_planner_agent,
            event_planner_agent,
            information_services_agent,
        ],
        config_list=config_list,
    )
    local_planner = LocalPlannerAgent(
        name="vacation_planner",
        model="gpt-3.5-turbo",
        children_agents=[
            travel_planner_agent,
            accomodation_dinning_planner_agent,
            event_planner_agent,
            information_services_agent,
        ],
        config_list=config_list,
    )

    # Brain Agent
    brain_agent = BrainAgent(
        name="brain",
        model="gpt-3.5-turbo",
        children_agents=[vacation_planner_agent, local_planner],
        config_list=config_list,
    )
