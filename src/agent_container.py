from autogen import config_list_from_models

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


class AgentContainer:
    config_list = config_list_from_models(model_list=config_model_list)

    # TODO: Add the LangchainAgent classes for the leaf agents
    # Currently they are all empty.
    # Google search, Google Maps, Google Places, Weather, Wikipedia, etc.

    # Travel Planner Agents
    long_distance_transportation_planner_agent = LongDistanceTransportationPlannerAgent(
        name="long_distance_transportation_planner",
        model="gpt-3.5-turbo",
        children_agents=[],
        config_list=config_list,
    )
    short_distance_transportation_planner_agent = (
        ShortDistanceTransportationPlannerAgent(
            name="short_distance_transportation_planner",
            model="gpt-3.5-turbo",
            children_agents=[],
            config_list=config_list,
        )
    )
    stop_planner_agent = StopPlannerAgent(
        name="stop_planner",
        model="gpt-3.5-turbo",
        children_agents=[],
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
    hotel_planner_agent = HotelPlannerAgent(
        name="hotel_planner",
        model="gpt-3.5-turbo",
        children_agents=[],
        config_list=config_list,
    )
    restaurant_planner_agent = RestaurantPlannerAgent(
        name="restaurant_planner",
        model="gpt-3.5-turbo",
        children_agents=[],
        config_list=config_list,
    )
    accomodation_dinning_planner_agent = AccomodationDinningPlannerAgent(
        name="accomodation_dinning_planner",
        model="gpt-3.5-turbo",
        children_agents=[hotel_planner_agent, restaurant_planner_agent],
        config_list=config_list,
    )

    # Event Planner Agents
    local_event_planner_agent = LocalEventPlannerAgent(
        name="local_event_planner",
        model="gpt-3.5-turbo",
        children_agents=[],
        config_list=config_list,
    )
    date_planner_agent = DatePlannerAgent(
        name="date_planner",
        model="gpt-3.5-turbo",
        children_agents=[],
        config_list=config_list,
    )
    touristic_attractions_planner_agent = TouristicAttractionsPlannerAgent(
        name="touristic_attractions_planner",
        model="gpt-3.5-turbo",
        children_agents=[],
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
    weather_agent = WeatherAgent(
        name="weather",
        model="gpt-3.5-turbo",
        children_agents=[],
        config_list=config_list,
    )
    cultural_information_agent = CulturalInformationAgent(
        name="cultural_information",
        model="gpt-3.5-turbo",
        children_agents=[],
        config_list=config_list,
    )
    emergency_agent = EmergencyInformationAgent(
        name="emergency",
        model="gpt-3.5-turbo",
        children_agents=[],
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
