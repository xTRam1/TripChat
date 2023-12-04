import http.client
import json
from typing import Any
from urllib.parse import quote


class BookingComClient:
    # Query Endpoints
    _FLIGHTS_SEARCH_LOCATION = "/api/v1/flights/searchDestination"
    _FLIGHTS_SEARCH = "/api/v1/flights/searchFlights"
    _TAXI_SEARCH_LOCATION = "/api/v1/taxi/searchLocation"
    _TAXI_SEARCH = "/api/v1/taxi/searchTaxi"
    _CAR_RENTAL_SEARCH_DESTINATION = "/api/v1/cars/searchDestination"
    _CAR_RENTAL_SEARCH = "/api/v1/cars/searchCarRentals"
    _CAR_RENTAL_VEHICLE_DETAILS = "/api/v1/cars/vehicleDetails"

    # Fields
    _rapid_api_host: str
    _rapid_api_key: str
    _headers: dict[str, str]
    _conn: http.client.HTTPSConnection

    def __init__(self, rapid_api_host: str, rapid_api_key: str):
        self._rapid_api_host = rapid_api_host
        self._rapid_api_key = rapid_api_key
        self._headers = {
            "X-RapidAPI-Key": self._rapid_api_key,
            "X-RapidAPI-Host": self._rapid_api_host,
        }
        self._conn = http.client.HTTPSConnection(self._rapid_api_host)

    def close(self) -> None:
        # Closes the http connections
        self._conn.close()

    #########
    # TOOLS #
    #########

    def flights_search_tool(
        self, departure_location: str, arrival_location: str, departure_date: str
    ) -> list[dict[str, Any]]:
        # Look up the flight search location ids
        from_id = self._flight_search_location(departure_location)
        to_id = self._flight_search_location(arrival_location)

        # Search for flights
        flights = self._flights_search(from_id, to_id, departure_date)

        return flights

    def car_rental_search_tool(
        self,
        location_query: str,
        pick_up_date: str,
        drop_off_date: str,
        pick_up_time: str,
        drop_off_time: str,
    ) -> dict[str, Any]:
        # Look up the car rental search location id
        coordinates = self._car_rental_search_destination(location_query)
        pick_up_latitude = drop_off_latitude = coordinates["latitude"]
        pick_up_longitude = drop_off_longitude = coordinates["longitude"]

        # Search for car rentals
        car_rentals = self._car_rental_search(
            pick_up_latitude,
            pick_up_longitude,
            drop_off_latitude,
            drop_off_longitude,
            pick_up_date,
            drop_off_date,
            pick_up_time,
            drop_off_time,
        )

        return {
            "info": {
                "pick_up_date": pick_up_date,
                "drop_off_date": drop_off_date,
                "pick_up_time": pick_up_time,
                "drop_off_time": drop_off_time,
            },
            "car_rentals": car_rentals,
        }

    #################
    # FLIGHT SEARCH #
    #################

    def _flight_search_location(self, query: str) -> str:
        query_params: dict[str, Any] = {"query": quote(query)}
        data = self._call_api(BookingComClient._FLIGHTS_SEARCH_LOCATION, query_params)

        if len(data) == 0:
            raise ValueError("No flight results found")

        # Get the first airport id
        return data[0]["id"]

    def _flights_search(
        self, from_id: str, to_id: str, depart_date: str
    ) -> list[dict[str, Any]]:
        query_params: dict[str, Any] = {
            "fromId": from_id,
            "toId": to_id,
            "departDate": depart_date,
            "sort": "CHEAPEST",
        }
        data = self._call_api(BookingComClient._FLIGHTS_SEARCH, query_params)

        # Get the first three flights
        # Need to get departure and arrival times and price
        flight_offers = data["flightOffers"]
        flights = flight_offers[: min(3, len(flight_offers))]
        results = []
        for flight in flights:
            segment = flight["segments"][0]
            departure_time = segment["departureTime"]
            arrival_time = segment["arrivalTime"]
            departure_airport = segment["departureAirport"]["name"]
            arrival_airport = segment["arrivalAirport"]["name"]

            legs = segment["legs"][0]
            airline_name = legs["carriersData"][0]["name"]
            flight_number = legs["flightInfo"]["flightNumber"]

            total_time = round(segment["totalTime"] / 3600, 2)
            total_price = flight["priceBreakdown"]["total"]["units"]

            results.append(
                {
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "airline": airline_name,
                    "departure_airport": departure_airport,
                    "arrival_airport": arrival_airport,
                    "flight_number": flight_number,
                    "total_time": str(total_time) + " hours",
                    "total_price": total_price,
                }
            )

        return results

    #####################
    # CAR RENTAL SEARCH #
    #####################

    def _car_rental_search_destination(self, query: str) -> dict[str, Any]:
        query_params: dict[str, Any] = {"query": query}
        data = self._call_api(
            BookingComClient._CAR_RENTAL_SEARCH_DESTINATION, query_params
        )

        if len(data) == 0:
            raise ValueError("No car results found")

        # Get coordinates of the first result
        return data[0]["coordinates"]

    def _car_rental_search(
        self,
        pick_up_latitude: float,
        pick_up_longitude: float,
        drop_off_latitude: float,
        drop_off_longitude: float,
        pick_up_date: str,
        drop_off_date: str,
        pick_up_time: str,
        drop_off_time: str,
    ) -> list[dict[str, Any]]:
        query_params: dict[str, Any] = {
            "pick_up_latitude": pick_up_latitude,
            "pick_up_longitude": pick_up_longitude,
            "drop_off_latitude": drop_off_latitude,
            "drop_off_longitude": drop_off_longitude,
            "pick_up_date": pick_up_date,
            "drop_off_date": drop_off_date,
            "pick_up_time": pick_up_time,
            "drop_off_time": drop_off_time,
        }
        data = self._call_api(BookingComClient._CAR_RENTAL_SEARCH, query_params)

        # We only care about the first three results
        # We get the vehicle info, route info, and price
        search_results = data["search_results"]

        if len(search_results) == 0:
            raise ValueError("No car results found")

        cars = search_results[: min(3, len(search_results))]
        results = []
        for car in cars:
            car_name = car["vehicle_info"]["v_name"]
            car_dropoff_address = car["route_info"]["dropoff"]["address"]
            car_pickup_address = car["route_info"]["dropoff"]["address"]
            price = car["pricing_info"]["price"]

            results.append(
                {
                    "car_name": car_name,
                    "car_dropoff_address": car_dropoff_address,
                    "car_pickup_address": car_pickup_address,
                    "price": price,
                }
            )

        return results

    ##################
    # HELPER METHODS #
    ##################

    def _call_api(self, endpoint: str, query_params: dict[str, Any]) -> Any:
        self._conn.request(
            "GET",
            self._build_query_string(endpoint, query_params),
            headers=self._headers,
        )
        res = self._conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        data = data.get("data", None)
        if data is None:
            raise ValueError("No data found")
        return data

    def _build_query_string(self, query: str, query_params: dict[str, Any]) -> str:
        query_string = "&".join(
            [f"{key}={value}" for key, value in query_params.items()]
        )
        return f"{query}?{query_string}"
