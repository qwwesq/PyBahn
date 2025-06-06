from .structs._internal import Journey, Station, Departure, Operator
from .config import Provider
import requests, typing
from .structs import Filter, Products
from datetime import datetime, timezone
from typing import Union, List



class PyBahn(object):
    """
    PyBahn is a client library for accessing Deutsche Bahn's unofficial public APIs.

    It allows querying:
    - Journeys between two stations
    - Departures from a station
    - Arrivals at a station
    - Nearby station
    """

    def __init__(self, import_name: str, provider: Provider = Provider.DB):
        """
        Initialize a PyBahn client.

        No authentication or configuration is required.
        This prepares the client to make requests to the Bahn API.
        """
        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip, deflate, br"
        }
        self.provider: Provider = provider

    def stations(self, name: str, limit: int = 10):
        """
        Searches for stations that match the given name and returns a list of Station objects.

        Args:
            name (str): The search keyword for station names.
            limit (int, optional): The maximum number of stations to return. Must be greater than 0. Defaults to 10.

        Returns:
            List[Station]: A list of Station objects matching the search criteria.

        Raises:
            ValueError: If the limit is less than 1.
            requests.RequestException: If the HTTP request fails.
        """

        if limit < 1:
            raise ValueError("Limit has to be more than 0")
        name = name.replace(" ", "+")
        url = f"https://int.bahn.de/web/api/reiseloesung/orte?suchbegriff={name}&typ=ALL&limit={limit}"

        response = requests.get(url, headers=self._headers)
        res_json: dict = response.json()
        _stations: typing.List[Station] = []

        for item in res_json:
            item: dict
            _stations.append(Station(name=item.get('name', ''), id=item.get('extId', ""), lid=item.get('id', ""), lat=item.get("lat", 0), lon=item.get('lon', 0), products=item.get('products', [])))
        
        return _stations

    def departures(self, id: Union[str, Station], filters: typing.List[Filter] = [Filter.RB_RE], duration: int = 180):
        """
        Returns a list of departures for a given station ID.

        Args:
            id (Union[str, Station]): The station ID for which to retrieve departures.
            filters (Optional[List[Filter]], optional): List of transport types to include in the results (e.g., ['train', 'bus']). Default is None.
            duration (Optional[int], optional): The duration (in minutes) to filter the departures. Default is None.

        Returns:
            List[Departure]: A list of `Departure` objects representing the departures from the station with the given `id`.
        """

        if isinstance(id, str):
            url_base = f"https://www.bahnhof.de/api/boards/departures?evaNumbers={id}"

        elif isinstance(id, Station):
            url_base = f"https://www.bahnhof.de/api/boards/departures?evaNumbers={id.id}"

        for filt in filters:
            url_base += filt

        if isinstance(duration, int):
            pass

        else:
            raise ValueError("Duration must be as int and more than 0")

        url = url_base + f"&duration={duration}&stationCategory=4&locale=en&sortBy=TIME_SCHEDULE"

        response = requests.get(url, headers=self._headers)
        res_json = response.json()
        deps: typing.List[Departure] = []

        for j in res_json['entries']:
            deps.append(Departure(**j[0]))

        return deps

    def arrivals(self, id: str, filters: typing.List[Filter] = [Filter.RB_RE], duration: int = 180):
        url_base = f"https://www.bahnhof.de/api/boards/arrivals?evaNumbers={id}"

        for filt in filters:
            url_base += filt

        url = url_base + f"&duration={duration}&stationCategory=4&locale=en&sortBy=TIME_SCHEDULE"
        response = requests.get(url, headers=self._headers)
        res_json = response.json()
        deps: typing.List[Departure] = []

        for j in res_json['entries']:
            deps.append(Departure(**j[0]))

        return deps

    def journeys(self, departure: typing.Union[str, Station], destination: typing.Union[str, Station], time: str = "now", products: typing.Union[typing.List[Products], Products] = Products.ALL, only_d_ticket: bool = False, stopovers: typing.List[Station] = []):
        """
        Retrieves a list of journey options between two locations.

        Args:
            departure (str): The location ID (LID) of the departure station(you can get it by using `station` function).
            destination (str): The location ID (LID) of the destination station(you can get it by using `station` function).
            time (str, optional): Desired departure time in ISO 8601 format (e.g., "2025-05-15T12:00:02"). 
                                If not provided (empty string), the current system time is used by default.
            products (Union[List[Products], Products], optional): Transport filters to limit the journey results 
                                (e.g., regional trains only). Can be a single product or a list. Defaults to `Products.REGIONALS`.
            only_d_ticket (bool, optional): If True, returns only journeys that are valid with the Deutschland-Ticket. Defaults to False.
            stopovers (List[Station], optional): List of stopovers stations, maximal is 2.
        """
        if time == "now":
            time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        url = "https://int.bahn.de/web/api/angebote/fahrplan"

        products = normalize_products(products)

        try:
            datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise ValueError("Wrong time format, please check again")
        

        data = {
            "abfahrtsHalt": departure if isinstance(departure, str) else departure.lid,
            "anfrageZeitpunkt": time,
            "ankunftsHalt": destination if isinstance(destination, str) else destination.lid,
            "ankunftSuche": "ABFAHRT",
            "klasse": "KLASSE_2",
            "produktgattungen": products,
            "reisende": [
                {
                    "typ": "JUGENDLICHER",
                    "ermaessigungen": [
                        {
                            "art": "KEINE_ERMAESSIGUNG",
                            "klasse": "KLASSENLOS"
                        }
                    ],
                    "alter": [],
                    "anzahl": 1
                }
            ],
            "schnelleVerbindungen": True,
            "sitzplatzOnly": False,
            "bikeCarriage": False,
            "reservierungsKontingenteVorhanden":False,
            "nurDeutschlandTicketVerbindungen": only_d_ticket,
            "deutschlandTicketVorhanden": False
        }

        if stopovers:
            if isinstance(stopovers, list):
                if len(stopovers) > 2:
                    raise ValueError("Too many stopovers, maximal is 2")
                else:
                    s_l_e_ = []

                    for d_sstop in stopovers:
                        if d_sstop.stopover_time and d_sstop.stopover_time > 0:
                            s_l_e_.append({
                                "id": d_sstop.lid,
                                "aufenthaltsdauer": d_sstop.stopover_time
                            })
                        else:
                            s_l_e_.append({
                                "id": d_sstop.lid
                            })

                    data['zwischenhalte'] = s_l_e_

            else:
                raise ValueError("Stopovers must be list even if 1")

        response = requests.post(url, headers=self._headers, json=data)
        res_json = response.json()
        journeys: typing.List[Journey] = []

        for jour in res_json['verbindungen']:
            __j = Journey(**jour)
            #__j.link = self.get_db_link(__j)
            for conn in __j.connections:
                if not conn.means_of_transport.direction:
                    conn.means_of_transport.direction = conn.arrival_station
            journeys.append(__j)

        return journeys

    def operators(self):
        url = f"https://int.bahn.de/web/api/angebote/stammdaten/verbuende"
        response = requests.get(url, headers=self._headers)
        res_json = response.json()
        l: typing.List[Operator] = []
        for d in res_json:
            l.append(Operator(**d))
        
        return l
    
    def get_db_link(self, journey: Journey) -> str:
        url = "https://int.bahn.de/web/api/angebote/verbindung/teilen"
        name_1 = journey.departure_name
        name_2 = journey.arrival_name
        if journey.connections[0].departure_time:
            ti = journey.connections[0].departure_time
            dt = datetime.strptime(ti, "%Y-%m-%dT%H:%M:%S")
            time_ = dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        else:
            time_ = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')

        ctx = journey.trip_lid

        r = requests.post(url, json={
            "startOrt": name_1,
            "zielOrt": name_2,
            "hinfahrtDatum": time_,
            "hinfahrtRecon": ctx
        }, headers=self._headers)

        if r.json()['vbid']:
            link = "https://int.bahn.de/en/buchung/start?vbid=" + r.json()['vbid']

            return link
        
        else:
            raise ValueError(r.text)

    def station(self, name: str):
        """
        Returns the first station that matches the given name.

        Args:
            name (str): The search keyword for the station name.

        Returns:
            Station: The first matching Station object.

        Raises:
            IndexError: If no stations are found.
        """
        station = self.stations(name, 2)
        if station[0].name.isupper():
            return station[1]
        else:
            return station[0]
    
    def nearby(self, latitude: float, longitude: float):
        url = f"https://int.bahn.de/web/api/reiseloesung/orte/nearby?lat={latitude}&long={longitude}&radius=9999&maxNo=100"

        response = requests.get(url, headers=self._headers)
        res_json: dict = response.json()
        _stations: typing.List[Station] = []

        for item in res_json:
            item: dict
            _stations.append(Station(name=item.get('name', None), id=item.get('extId', None), lid=item.get('id', None), lat=item.get("lat", 0), lon=item.get('lon', 0), products=item.get('products', [])))
        
        return _stations

__all__ = ["PyBahn"]


def normalize_products(products: Union[List[Union[Products, str]], Products, str]) -> List[str]:
    if isinstance(products, Products):
        products = products.value if isinstance(products.value, list) else [products.value]
    elif isinstance(products, list):
        result = []
        for item in products:
            if isinstance(item, Products) and isinstance(item.value, list):
                result.extend(item.value)
            elif isinstance(item, Products):
                result.append(item.value)
            elif isinstance(item, str):
                result.append(item)
        return result
    
    else:
        raise ValueError("Wrong `products` parameter, please check again")
    return products


if __name__ == "__main__":
    raise RuntimeError("This module is not intended to be run or imported directly.")
