from autogen.agentchat.agent import Agent
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat.groupchat import GroupChat

TEAMS = {
    "EventPlanning": ["LocalEventSearch", "TouristicAttractionFinder"],
    "Logistics": ["TransportationPlanner", "HotelAirbnbPlanner"],
    "Information": ["CulturalInsights", "Weather"],
    "Brain": ["Brain", "TerminationUserProxy"],
}

AGENT_TO_TEAM_NAME = {
    "HeadofEventPlanning": "EventPlanning",
    "LocalEventSearch": "EventPlanning",
    "TouristicAttractionFinder": "EventPlanning",
    "HeadofLogistics": "Logistics",
    "TransportationPlanner": "Logistics",
    "HotelAirbnbPlanner": "Logistics",
    "HeadofInformation": "Information",
    "CulturalInsights": "Information",
    "Weather": "Information",
    "Brain": "Brain",
    "TerminationUserProxy": "Brain",
}

TEAM_LEADER_NAMES = ["HeadofEventPlanning", "HeadofLogistics", "HeadofInformation"]

CUSTOM_GROUP_CHAT_SYSTEM_MESSAGE = [
    "Everyone cooperate and help agent Brain in his task of generating a good trip plan with the following template: \n"
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
    "you MUST select Brain as the next speaker which will get more information from the user and get back to you."
]


class CustomGroupChat(GroupChat):
    def __init__(self, agents, messages, max_round=10):
        super().__init__(agents, messages, max_round)
        self.team_mapping = {team: 0 for team in TEAMS.keys()}
        self.team_leader_index = 0

    def select_speaker(self, last_speaker: Agent, selector: AssistantAgent) -> Agent:
        if last_speaker.name == "Brain":
            return self.agent_by_name(TEAM_LEADER_NAMES[self.team_leader_index])

        # Check if the last_speaker is a team leader
        # if it is a team leader, then return the first child teammate
        last_speaker_name = last_speaker.name
        team_name = AGENT_TO_TEAM_NAME[last_speaker_name]
        if last_speaker_name in TEAM_LEADER_NAMES:
            next_child_teammate_index = self.team_mapping[team_name]
            self.team_mapping[team_name] += 1

            child_teammates = TEAMS[team_name]
            return self.agent_by_name(child_teammates[next_child_teammate_index])

        # if it is child teammate already, call the next child teammate
        # if there is no child teammate, pick another team leader
        # if there is no team leader, give the turn to the brain
        else:
            child_teammates = TEAMS[team_name]
            next_child_teammate_index = self.team_mapping[team_name]
            self.team_mapping[team_name] += 1

            if next_child_teammate_index < len(child_teammates):
                return self.agent_by_name(child_teammates[next_child_teammate_index])
            else:
                self.team_leader_index += 1
                if self.team_leader_index >= len(TEAM_LEADER_NAMES):
                    self.team_mapping = {team: 0 for team in TEAMS.keys()}
                    self.team_leader_index = 0
                    return self.agent_by_name("Brain")
                next_team_leader = TEAM_LEADER_NAMES[self.team_leader_index]
                return self.agent_by_name(next_team_leader)
