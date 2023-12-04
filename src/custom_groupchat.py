CUSTOM_GROUP_CHAT_SYSTEM_MESSAGE = [
    {
        "role": "system",
        "content": "Everyone cooperate and help agent Brain in his task of generating a good trip plan with the following template: \n"
        """{"EventPlanning": {
      "LocalEventSearch": {
        "LocalEvents": {
          "Event1": {
            "Name": "",
            "Description": "",
            "Date": "",
            "Location": "",
            "Link": ""
            #// Additional events can be added in a similar format
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
            #// Additional attractions can be added in a similar format
          }
        }
      }
    },
    "Logistics": {
      "TransportationPlanner": {
        "TransportationDetails": {
          "Flights": "",
          "Trains": "",
          "Buses": "",
          "CarRentals": "",
          "IntraCityTravel": ""
        }
      },
      "HotelAirbnbPlanner": {
        "AccommodationDetails": {
          "Name": "",
          "Address": "",
          "ContactInfo": "",
          "CheckIn": "",
          "CheckOut": "",
          "Amenities": "",
          "Link": ""
      }
    },
    "Information": {
      "CulturalInsights": {
          "Customs": "",
          "LanguageTips": "",
          "Cuisine": ""
      },
      "Weather": {
          "WeatherForecast": "",
          "WeatherWarnings": ""
        },
    }
  }
}"""
        "Team EventPlanning has HeadofEventPlanning, LocalEventSearch, TouristicAttractionFinder. "
        "Team Logistics has HeadofLogistics, TransportationPlanner, HotelAirbnbPlanner. "
        "Only members of the same team can talk to one another. Only team leaders (names starting with Head) "
        "can talk amongst themselves. When an agent seems to ask for an extra user input or some kind of information from the user, "
        "you MUST select Brain as the next speaker which will get more information from the user and get back to you.",
    }
]
