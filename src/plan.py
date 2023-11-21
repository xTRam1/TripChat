from typing import Any

plan_template = {
    "EventPlanning": {
        "LocalEventSearch": {
            "LocalEvents": {
                "Event1": {
                    "Name": "",
                    "Description": "",
                    "Date": "",
                    "Location": "",
                    "Link": ""
                    # // Additional events can be added in a similar format
                }
            }
        },
        "TouristicAttractionFinder": {
            "TouristicAttractions": {
                "Attraction1": {
                    "Name": "",
                    "Description": "",
                    "OpeningHours": "",
                    "EntryFee": ""
                    # // Additional attractions can be added in a similar format
                }
            }
        },
    },
    "Logistics": {
        "TransportationPlanner": {
            "FlightDetails1": {
                "DepartureTime": "",
                "ArrivalTime": "",
                "DepartureAirport": "",
                "ArrivalAirport": "",
                "FlightNumber": "",
                "Airline": "",
                "TotalTime": "",
                "TotalPrice": "",
                # // Additional flight details can be added in a similar format
            },
            "CarRentalDetails1": {
                "PickUpAddress": "",
                "PickUpTime": "",
                "DropOffAddress": "",
                "DropOffTime": "",
                "VehicleName": "",
                "TotalPrice": "",
                # // Additional car rental details can be added in a similar format
            },
        },
        "HotelAirbnbPlanner": {
            "AccommodationDetails": {
                "Name": "",
                "Address": "",
                "ContactInfo": "",
                "CheckIn": "",
                "CheckOut": "",
                "Amenities": "",
                "Link": "",
            }
        },
    },
    "Information": {
        "CulturalInsights": {"Customs": "", "LanguageTips": "", "Cuisine": ""},
        "Weather": {"WeatherForecast": "", "WeatherWarnings": ""},
    },
}


def get_travel_plan_template():
    return plan_template


def update_travel_plan(section: str, data: dict[str, Any]):
    """
    Update the travel plan template with the provided data for the specified section.

    :param template: The travel plan template (a dictionary).
    :param section: The section to be updated (string). Example: 'EventPlanning.LocalEventSearch'.
    :param data: The data to update the section with (a dictionary).
    :return: Updated travel plan template.
    """

    # Split the section into parts (to handle nested sections)
    parts = section.split(".")

    # Reference to the part of the template being updated
    current_section = plan_template

    # Iterate through the parts to reach the desired section
    for part in parts:
        if part in current_section:
            current_section = current_section[part]
        else:
            raise ValueError(f"Section '{part}' not found in the template")

    # Update the relevant section with the provided data
    current_section.update(data)

    return plan_template


get_travel_plan_template_schema = {
    "name": "get_travel_plan_template",
    "description": "Get the travel plan template.",
    "parameters": {},
}

update_function_schema = {
    "name": "update_travel_plan",
    "description": "Update the travel plan template with the provided data for the specified section.",
    "parameters": {
        "type": "object",
        "properties": {
            "section": {
                "type": "string",
                "description": "The section to be updated in the travel plan template, in dot notation. Example: 'EventPlanning.LocalEventSearch'",
            },
            "data": {
                "type": "object",
                "description": "The data to update the specified section with, structured as a dictionary.",
            },
        },
        "required": ["section", "data"],
    },
}

update_function = {"update_travel_plan": update_travel_plan}
get_travel_plan_template_function = {
    "get_travel_plan_template": get_travel_plan_template
}
